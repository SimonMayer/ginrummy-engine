export function setErrorMessage(context, title, error) {
    context.errorTitle = title;
    context.errorMessage = error.response?.data?.error || error.message || '';
}

export function clearErrorMessage(context) {
    context.errorTitle = '';
    context.errorMessage = '';
}
