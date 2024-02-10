# _*_ coding: utf-8 _*_

import pdfsplitter




def upload():
    """
    Funkcja upload.
    :return:
    Funkcja rodzielająca plik pdf na plik 1 stronicowe, 2 stronicowe lub wielo. Dodatkowo nadaje nazwę tym plikom
    Zapisuje również do pliku każdą aktualizację.
    """
    if request.method == "POST":
        try:
            f = request.files["file"]
            customFolder = request.form["customFolder"]
            customSuffix = request.form["customSuffix"]

            if customFolder[-1] != "\\":
                customFolder += "\\"

            customSplitPages = int(request.form["customSplitPages"])

            if customSplitPages == 0:
                customSplitPages = int(request.form["customSplitPagesDefined"])

            upload.file_name = f.filename

            f.save(f"{customFolder}{upload.file_name}")
            data = pdfsplitter.splitPDF(f"{customFolder}{upload.file_name}", customSplitPages, customSuffix)

            return render_template("splitter/file_upload.html",
                                   data=[request.method, data, customFolder, customSplitPages])
        except Exception as e:
            return render_template("splitter/file_upload.html", data=[request.method, e])
    else:
        return render_template("splitter/file_upload.html", data=[request.method])
