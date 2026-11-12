from pathlib import Path
from textwrap import wrap

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Preformatted, KeepTogether,
)
from reportlab.graphics.shapes import Drawing, Rect, Circle, Polygon, String, Path as ShapePath
from reportlab.lib.colors import HexColor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "Titanic_Survivor_Data_Preparation_Project.pdf"
CODE = ROOT / "outputs" / "titanic_preparation_pipeline.py"

NAVY = HexColor("#18324B")
BLUE = HexColor("#2F6690")
PALE = HexColor("#EAF1F6")
INK = HexColor("#24313B")
MUTED = HexColor("#5B6770")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="ProjectTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=23, leading=28, textColor=NAVY, alignment=TA_CENTER, spaceAfter=7))
styles.add(ParagraphStyle(name="Subtitle", parent=styles["Normal"], fontName="Helvetica", fontSize=11, leading=15, textColor=MUTED, alignment=TA_CENTER, spaceAfter=15))
styles.add(ParagraphStyle(name="Byline", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=BLUE, alignment=TA_CENTER, spaceAfter=8))
styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=NAVY, spaceBefore=9, spaceAfter=8, keepWithNext=True))
styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=BLUE, spaceBefore=7, spaceAfter=4, keepWithNext=True))
styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.3, leading=13.5, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name="Smallx", parent=styles["BodyText"], fontName="Helvetica", fontSize=8, leading=10.5, textColor=INK, spaceAfter=3))
styles.add(ParagraphStyle(name="Cellx", parent=styles["BodyText"], fontName="Helvetica", fontSize=8, leading=10.5, textColor=INK))
styles.add(ParagraphStyle(name="HeaderCellx", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=8, leading=10.5, textColor=colors.white))
styles.add(ParagraphStyle(name="CodeCaption", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=8.2, leading=11, textColor=BLUE, spaceBefore=5, spaceAfter=3))

def p(text, style="Bodyx"):
    return Paragraph(text, styles[style])

def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    if doc.page > 1:
        canvas.setStrokeColor(HexColor("#D7E0E6"))
        canvas.setLineWidth(0.5)
        canvas.line(19*mm, h-14*mm, w-19*mm, h-14*mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(19*mm, h-11*mm, "TITANIC SURVIVOR DATA PREPARATION PIPELINE")
    canvas.setStrokeColor(HexColor("#D7E0E6"))
    canvas.line(19*mm, 13*mm, w-19*mm, 13*mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(w-19*mm, 8.5*mm, f"{doc.page}")
    canvas.restoreState()

doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=19*mm, rightMargin=19*mm, topMargin=20*mm, bottomMargin=19*mm, title="Titanic Survivor Data Preparation Pipeline", author="")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id="main", frames=frame, onPage=header_footer)])
story = []

def titanic_illustration():
    """Draw a compact, print-friendly Titanic and iceberg illustration."""
    d = Drawing(480, 78)
    d.add(Rect(0, 0, 480, 78, fillColor=HexColor("#F0F6FA"), strokeColor=HexColor("#D9E6EE"), strokeWidth=0.6, rx=8, ry=8))
    d.add(Circle(380, 61, 8, fillColor=HexColor("#E7B96A"), strokeColor=None))
    # Distant water and iceberg
    d.add(Polygon([353, 18, 369, 57, 379, 39, 391, 61, 405, 18], fillColor=HexColor("#B8D9E8"), strokeColor=HexColor("#91BFD4"), strokeWidth=0.7))
    d.add(Polygon([367, 18, 371, 38, 379, 32, 387, 18], fillColor=HexColor("#D8EAF2"), strokeColor=None))
    # Small prepared-data sheet to pair the maritime scene with the project topic.
    d.add(Rect(425, 19, 35, 46, fillColor=colors.white, strokeColor=HexColor("#91BFD4"), strokeWidth=0.8, rx=2, ry=2))
    d.add(Rect(430, 54, 25, 5, fillColor=BLUE, strokeColor=None))
    d.add(String(432, 55, "CSV", fontName="Helvetica-Bold", fontSize=4.5, fillColor=colors.white))
    for y in (47, 40, 33, 26):
        d.add(Rect(431, y, 5, 3, fillColor=HexColor("#D6E7F0"), strokeColor=None))
        d.add(Rect(439, y+1, 16, 1.4, fillColor=HexColor("#8DA9B7"), strokeColor=None))
    # Ship hull, deck and portholes
    d.add(Polygon([49, 31, 337, 31, 321, 17, 82, 17], fillColor=NAVY, strokeColor=NAVY, strokeWidth=0.8))
    d.add(Rect(82, 31, 220, 8, fillColor=HexColor("#F8F7F2"), strokeColor=None))
    d.add(Rect(122, 39, 132, 9, fillColor=HexColor("#E6E3DA"), strokeColor=None))
    d.add(Rect(152, 48, 77, 7, fillColor=HexColor("#F8F7F2"), strokeColor=None))
    for x in (151, 176, 201, 226, 251, 276):
        d.add(Circle(x, 25, 1.2, fillColor=HexColor("#E8BD72"), strokeColor=None))
    for x in (156, 181, 206, 231, 256, 281):
        d.add(Rect(x, 34, 11, 2.2, fillColor=BLUE, strokeColor=None))
    for x in (168, 194, 220):
        d.add(Rect(x, 41.5, 10, 2, fillColor=BLUE, strokeColor=None))
    # Four funnels with warm caps
    for x in (145, 174, 203, 232):
        d.add(Rect(x, 55, 12, 17, fillColor=HexColor("#D4C9B4"), strokeColor=None))
        d.add(Rect(x, 68, 12, 4, fillColor=HexColor("#B66A46"), strokeColor=None))
    # Layered waves
    for y, x0, x1 in ((13, 22, 360), (8, 59, 384), (4, 17, 342)):
        path = ShapePath()
        path.moveTo(x0, y)
        path.curveTo(x0+22, y+4, x0+40, y-3, x0+62, y)
        path.lineTo(x1, y)
        path.strokeColor = HexColor("#7EACC4")
        path.strokeWidth = 0.9
        path.fillColor = None
        d.add(path)
    d.add(String(17, 59, "TITANIC", fontName="Helvetica-Bold", fontSize=7, fillColor=NAVY))
    return d

story += [Spacer(1, 3*mm), p("Titanic Survivor Data Preparation Pipeline", "ProjectTitle"), p("Minor Project | Machine Learning Data Preparation", "Subtitle"), p("Name: Sri Santhosh R", "Byline")]
meta = [[p("PROJECT AREA", "Smallx"), p("DELIVERABLE", "Smallx"), p("DATASET", "Smallx")],
        [p("Data cleaning and feature preparation", "Cellx"), p("Runnable Python script and prepared CSV outputs", "Cellx"), p("Seaborn Titanic example dataset", "Cellx")]]
t = Table(meta, colWidths=[55*mm, 64*mm, 51*mm])
t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),PALE),("TEXTCOLOR",(0,0),(-1,0),NAVY),("GRID",(0,0),(-1,-1),0.45,HexColor("#D9D9D9")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
story += [t, Spacer(1, 2*mm), titanic_illustration(), Spacer(1, 1*mm), p("Project overview", "H1x"), p("This project prepares the Titanic passenger dataset for downstream machine learning. A maritime historian needs clean, encoded, scaled, and split data for later survival analysis. The pipeline validates and cleans inputs, removes leakage and redundant fields, handles missing values, creates a stratified 80/20 split, encodes categories, and scales features. It stops before model training and saves reusable feature/label CSV files.")]
story += [p("Objectives", "H2x"), p("Preserve the survival labels, avoid target leakage, and make preprocessing reproducible for unseen data. The complete implementation appears in the appendix; no prediction model is trained or evaluated.")]

story += [p("1. Dataset and preparation design", "H1x"), p("The source is Seaborn's example dataset named <b>titanic</b>. Its target is <b>survived</b> (0 = did not survive, 1 = survived). The preparation uses passenger and voyage attributes such as class, sex, age, family counts, fare, and embarkation. Seaborn downloads the data from its example-data repository when it is not cached, so first-time use requires an internet connection.")]
rows = [[p("Field", "HeaderCellx"), p("Treatment", "HeaderCellx"), p("Reason", "HeaderCellx")],
 [p("survived", "Cellx"), p("Kept separately as y", "Cellx"), p("Target label for later supervised learning", "Cellx")],
 [p("alive", "Cellx"), p("Removed", "Cellx"), p("Text duplicate of the target; would leak the answer", "Cellx")],
 [p("deck", "Cellx"), p("Removed", "Cellx"), p("Mostly missing and not needed for this exercise", "Cellx")],
 [p("class / embark_town", "Cellx"), p("Removed", "Cellx"), p("Duplicate representations of pclass / embarked", "Cellx")],
 [p("sex / alone / adult_male", "Cellx"), p("Binary numeric", "Cellx"), p("Two-level fields become numeric indicators", "Cellx")],
 [p("pclass", "Cellx"), p("Retained as ordinal numeric", "Cellx"), p("Passenger classes have a natural order", "Cellx")],
 [p("embarked / who", "Cellx"), p("One-hot encoded", "Cellx"), p("Nominal categories have no numeric order", "Cellx")]]
t = Table(rows, colWidths=[37*mm, 48*mm, 85*mm], repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),0.4,HexColor("#D9D9D9")),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,HexColor("#F5F8FA")]),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
story += [t, Spacer(1, 3*mm), p("Data handling note", "H2x"), p("The train/test split occurs before imputation, category encoding, and scaling. The test set is transformed using rules learned from the training set, so test observations do not influence medians, modes, one-hot columns, means, or standard deviations. This ordering preserves a fair downstream evaluation.")]

story += [p("2. Pipeline steps", "H1x")]
steps = [
 ("1", "load_data()", "Load the Seaborn Titanic table. A clear error explains that dataset access may need internet."),
 ("2", "validate_data()", "Require the target and key input fields, reject empty data, null targets, and unexpected target values."),
 ("3", "clean_text()", "Trim whitespace and lowercase string categories without changing numeric or boolean columns."),
 ("4", "drop_useless()", "Remove alive (target leakage), deck (mostly missing), and duplicated class/embark_town fields."),
 ("5", "split_data()", "Create an 80/20 split with random_state=42 and stratify=survived, preserving class proportions."),
 ("6", "handle_missing()", "Use training medians for numeric columns and training modes for categorical columns; reuse them on test."),
 ("7", "encode_categoricals()", "Map binary fields, retain ordinal pclass, and one-hot encode embarked and who. Align test columns to training."),
 ("8", "scale_features()", "Fit StandardScaler on training inputs, then transform train and test using the same parameters."),
 ("-", "main()", "Call functions in order, save the two CSVs, and report validation/runtime failures in a readable way."),
]
rows=[[p("Step", "HeaderCellx"),p("Function", "HeaderCellx"),p("Action", "HeaderCellx")]]+[[p(a,"Cellx"),p(b,"Cellx"),p(c,"Cellx")] for a,b,c in steps]
t=Table(rows,colWidths=[14*mm,47*mm,109*mm],repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),0.4,HexColor("#D9D9D9")),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,HexColor("#F5F8FA")]),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
story += [t, Spacer(1, 3*mm), p("Why scaling is included", "H2x"), p("Standardization converts each numeric feature using z = (x - mean) / standard deviation. It helps many downstream algorithms that are sensitive to feature scale. Some tree-based models do not require it, but the assignment asks for a scaled dataset, so the same prepared output can support scale-sensitive methods.")]

story += [p("3. Uses and limitations", "H1x"), p("Uses", "H2x"), p("- Provides consistent input for later classification experiments such as logistic regression, nearest neighbors, or support vector machines.<br/>- Demonstrates a reusable preprocessing workflow with a target-preserving split.<br/>- Produces tabular CSVs that can be inspected, shared, and passed to downstream training code.<br/>- Shows how to guard against leakage from both direct target copies and fitted preprocessing statistics.")]
story += [p("Limitations", "H2x"), p("This is an educational preparation pipeline, not a validated safety-critical or historical inference system. The example dataset is small and has known collection and representativeness limits. Removing deck discards potentially useful information because it is heavily incomplete. Mode imputation and one-hot encoding are straightforward baseline choices, not universally optimal. The script does not persist preprocessing objects; for production inference, save a fitted pipeline so new records receive exactly the same transformations.")]

story += [p("4. Setup and execution", "H1x"), p("Requirements", "H2x"), p("Python 3.9 or newer is recommended. Install pandas, seaborn, and scikit-learn in the active Python environment:")]
story += [Preformatted("python -m pip install pandas seaborn scikit-learn", ParagraphStyle("cmd", fontName="Courier", fontSize=8.5, leading=12, textColor=NAVY, backColor=PALE, borderPadding=7, leftIndent=7, rightIndent=7, spaceBefore=2, spaceAfter=8))]
story += [p("Run", "H2x"), Preformatted("python titanic_preparation_pipeline.py", ParagraphStyle("cmd2", fontName="Courier", fontSize=8.5, leading=12, textColor=NAVY, backColor=PALE, borderPadding=7, leftIndent=7, rightIndent=7, spaceBefore=2, spaceAfter=8))]
story += [p("The source script and current directory must be writable so the CSV files can be saved. If dataset download fails, check the connection or adapt load_data() to read a local Titanic CSV with pandas.read_csv(). The local file must contain the required columns listed in validate_data().")]
story += [p("Expected result", "H2x"), p("The console prints the row counts and prepared feature count, and creates titanic_train_prepared.csv and titanic_test_prepared.csv. The precise feature count depends on categories present in the downloaded dataset. The output target column remains integer-valued; transformed features are standardized numeric values.")]

story += [p("5. Resources used", "H1x")]
resources = [
 ("Dataset loader", "Seaborn load_dataset API", "https://seaborn.pydata.org/generated/seaborn.load_dataset.html"),
 ("Dataset repository", "Seaborn example data (Titanic CSV)", "https://github.com/mwaskom/seaborn-data/blob/master/titanic.csv"),
 ("Train/test split", "scikit-learn train_test_split", "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html"),
 ("Feature scaling", "scikit-learn StandardScaler", "https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html"),
 ("Categorical encoding", "scikit-learn preprocessing guide", "https://scikit-learn.org/stable/modules/preprocessing.html"),
]
rows=[[p("Purpose","HeaderCellx"),p("Resource","HeaderCellx"),p("Reference","HeaderCellx")]]
for purpose,title,url in resources:
    rows.append([p(purpose,"Cellx"),p(title,"Cellx"),Paragraph(f'<link href="{url}" color="#2F6690">{url}</link>',styles["Cellx"])])
t=Table(rows,colWidths=[34*mm,53*mm,83*mm],repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),0.4,HexColor("#D9D9D9")),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,HexColor("#F5F8FA")]),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
story += [t, Spacer(1, 3*mm), p("Libraries", "H2x"), p("pandas is used for tabular data and CSV export; seaborn loads the Titanic sample; scikit-learn supplies the stratified split and StandardScaler. Python standard-library modules provide exception handling and type annotations.")]

story += [p("6. Conclusion", "H1x"), p("The project turns a raw Titanic sample into clean, encoded, scaled training and test datasets while keeping the survival label available for downstream learning. Its central design choice is to split first and fit preprocessing steps on training data only. The result is a compact, modular example of responsible data preparation; no prediction model or performance claim is included.")]

story += [PageBreak(), p("Appendix A Complete Python Code", "H1x"), p("This is the complete runnable script delivered with the report. Save the appendix code as titanic_preparation_pipeline.py, or use the separate Python file included with this project.")]

code = CODE.read_text(encoding="utf-8").splitlines()
code_style = ParagraphStyle("CodeBlock", fontName="Courier", fontSize=6.55, leading=8.1, textColor=HexColor("#202830"), leftIndent=0, rightIndent=0, spaceAfter=0)
max_chars = 101
for line in code:
    # Soft wrap long source lines while preserving continuation indentation.
    if len(line) <= max_chars:
        story.append(Preformatted(line or " ", code_style, maxLineLength=max_chars))
    else:
        indent = len(line) - len(line.lstrip())
        chunks = wrap(line, width=max_chars, subsequent_indent=" " * min(indent + 4, 20), break_long_words=True, break_on_hyphens=False)
        for chunk in chunks:
            story.append(Preformatted(chunk, code_style, maxLineLength=max_chars))

doc.build(story)
print(OUT)
