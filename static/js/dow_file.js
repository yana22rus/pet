let count = 0

function dow_file() {
    let form = document.querySelector("#form_data")
    let input = document.createElement("input")
    input.setAttribute("id", count)
    input.setAttribute("name", `file_${count}`)
    input.setAttribute("accept", "application/pdf")
    input.type = "file"
    form.appendChild(input)
    input.click()
    count += 1
}
