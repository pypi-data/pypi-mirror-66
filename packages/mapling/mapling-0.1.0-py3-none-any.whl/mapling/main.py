import typer
import pandas as pd
from pathlib import Path
import random
import requests
import json
import textract

import spacy
from spacy.tokens import Span
from spacy import displacy
from spacy.matcher import Matcher

app = typer.Typer()


def python_matcher(text, term):
    index = 0
    matches = []
    while True:
        index = text.find(term, index + 1)
        matches.append((index, index + len(term), term))
        if index == -1:
            break
    return matches[:-1]


@app.command()
def process(
    documents_folder: str,
    gazetteer: str = None,
    model: str = None,
    html: bool = False,
    output: str = Path.cwd().as_posix(),  #current path
):
    data = []
    if not Path(output).exists():
        Path(output).mkdir(parents=True, exist_ok=True)
        message = typer.style(
            "🌞 Creating a new directory: " + output,
            fg=typer.colors.RED,
            bold=True,
        )
        typer.echo(message)

    if gazetteer:
        places = []
        with open(gazetteer) as f:
            for line in f:
                places.append(line.replace("\n", ""))
        files = Path(documents_folder).iterdir()
        with typer.progressbar(files, label="🎠 Processing gazetteer") as progress:
            for file in progress:
                text = textract.process(file).decode("utf-8")
                for place in places:
                    match = python_matcher(text, place)
                    if match:
                        for start, end, place in match:
                            row = {}
                            row["file"] = file.name
                            row["start"] = start
                            row["end"] = end
                            row["place"] = place
                            row["label"] = "GAZ"
                            data.append(row)

    if model:

        try:
            nlp = spacy.load(model)
            if not "ner" in nlp.pipe_names:
                spacy_link = typer.style(
                    "https://spacy.io/models", fg=typer.colors.MAGENTA, bold=True
                )
                error = typer.style(
                    "🍊 Please use a model with an ner pipeline.  See: " + spacy_link,
                    fg=typer.colors.RED,
                    bold=True,
                )
                typer.echo(error)
                raise typer.Exit()

            else:
                files = Path(documents_folder).iterdir()
                with typer.progressbar(files, label="🍁 Processing model") as progress:
                    for file in progress:
                        text = textract.process(file).decode("utf-8")
                        doc = nlp(text)
                        for ent in doc.ents:

                            row = {}
                            row["file"] = file.name
                            row["start"] = ent.start_char
                            row["end"] = ent.end_char
                            row["place"] = ent.text.replace("\n", "")
                            row["label"] = ent.label_
                            data.append(row)

        except OSError:
            version = spacy.__version__
            models = requests.get(
                "https://raw.githubusercontent.com/explosion/spacy-models/master/compatibility.json"
            )
            models = json.loads(models.text)
            models = models["spacy"][version].keys()
            if model in models:
                command = typer.style(
                    f"$ python -m spacy download {model}",
                    fg=typer.colors.BRIGHT_CYAN,
                    bold=True,
                )
                typer.echo(
                    f"🌻 That spaCy model needs to be downloaded.  Please enter "
                    + command
                )
                raise typer.Exit()
            else:
                spacy_link = typer.style(
                    "https://spacy.io/models", fg=typer.colors.BRIGHT_MAGENTA, bold=True
                )
                typer.echo(
                    f"🎌 Please enter a valid spaCy model name. See " + spacy_link
                )
                raise typer.Exit()

    if html and model or gazetteer:
        nlp = spacy.blank("en")
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
        colors = {}
        options = {"ents": [], "colors": colors}
        palette = ["#70ffdf", "#ff4df0", "#2bd1fc", "#c04df9"]

        for row in data:
            hex1 = random.choice(palette)
            hex2 = random.choice(palette)
            colors[row["label"]] = f"linear-gradient(90deg, {hex1}, {hex2})"
            options["ents"].append(row["label"])
            ner.add_label(row["label"])
        nlp.begin_training()
        matcher = Matcher(nlp.vocab)
        for row in data:
            name = row["place"]
            pattern = [{"TEXT": f"{name}"}]
            matcher.add(row["label"], None, pattern)

        files = Path(documents_folder).iterdir()
        for file in files:
            text = textract.process(file).decode("utf-8")
            doc = nlp(text)
            matches = matcher(doc)
            typer.echo(f"Processing html for {file.name}")
            with typer.progressbar(matches) as progress:
                for match_id, start, end in progress:
                    span = Span(doc, start, end, label=match_id)
                    try:
                        doc.ents = list(doc.ents) + [span]
                    except ValueError:  # [E103] Trying to set conflicting doc.ents
                        pass

            html = displacy.render(doc, style="ent", page=True, options=options)

            output_path = Path(output) / f"{file.name.split('.')[0]}.html"
            output_path.open("w", encoding="utf-8").write(html)
            success = typer.style(
                "🌵 Created file: ", fg=typer.colors.BRIGHT_GREEN, bold=True
            )
            typer.echo(success + output_path.name)
    else:
        need_something = typer.style(
            "🌮 Please select a gazetteer or spaCy model", fg=typer.colors.BRIGHT_GREEN, bold=True
        )
        typer.echo(need_something)
        raise typer.Exit()

    if data:
        df = pd.DataFrame(data)
        df.to_csv(output + 'output.csv', index=False)
        success = typer.style(
            "🌱 Created file: ", fg=typer.colors.BRIGHT_GREEN, bold=True
        )
        typer.echo(success + output + '/output.csv')


if __name__ == "__main__":
    app()
