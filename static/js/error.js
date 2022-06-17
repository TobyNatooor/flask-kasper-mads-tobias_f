
const params = new URLSearchParams(window.location.search)
if (params.has("errorMessage")) {
    errorMessage = params.get("errorMessage")
    alert(errorMessage)
}
