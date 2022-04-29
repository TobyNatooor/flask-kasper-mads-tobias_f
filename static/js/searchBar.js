
searchBar = document.querySelector('#search-bar')
trainsHtml = document.querySelector('.train-frames').children
trainIDs = []
for (let trainHtml of trainsHtml) {
    trainIDs.push(trainHtml.innerText)
}
searchBar.addEventListener('change', () => {
    for (let trainID of trainIDs) {
        htmlEl = document.querySelector("#" + trainID)
        if (trainID.toLowerCase().includes(searchBar.value.toLowerCase())) {
            htmlEl.style.display = "flex"
        } else {
            htmlEl.style.display = "none"
        }
    }
})
