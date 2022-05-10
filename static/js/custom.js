let labels = document.getElementsByClassName("custom-file-upload");
let customFilesUpload = Array.from(labels).map(label => $(`input[id="${label.htmlFor}"]`)[0])

let replaceAfterUpload = function () {
    let fileObject = this.files[0];
    let fileName = fileObject.name.split("\\");
    let label = $(`label[for="${this.id}"]`)[0];
    label.innerText = fileName[fileName.length - 1];
}

Array.from(customFilesUpload).forEach(function (element) {
    element.addEventListener('change', replaceAfterUpload);
});