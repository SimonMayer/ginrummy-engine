export function formatDateTime(dateTimeString) {
    const date = new Date(dateTimeString);
    return new Intl.DateTimeFormat(navigator.language, {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    }).format(date);
}
