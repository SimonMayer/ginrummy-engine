import { refreshSseToken } from './tokenService';

const BASE_URL = process.env.VUE_APP_BASE_URL;

class SSEService {
    constructor(endpoint, maxRetries = 3, retryDelay = 1000) {
        this.endpoint = endpoint;
        this.maxRetries = maxRetries;
        this.retryDelay = retryDelay;
        this.eventSource = null;
        this.retryCount = 0;
        this.forcedClose = false; // To track if the close was forced
    }

    async createUrl() {
        let token = localStorage.getItem('sse_access_token');
        if (!token) {
            token = await refreshSseToken();
        }

        const url = new URL(`${BASE_URL}${this.endpoint}`);
        url.searchParams.set('token', token);

        return url.toString();
    }

    async connect(onMessage, onError) {
        try {
            this.url = await this.createUrl();
            this.eventSource = new EventSource(this.url);

            this.eventSource.onopen = () => {
                this.retryCount = 0; // Reset retry count on successful connection
            };

            this.eventSource.onmessage = (event) => {
                if (onMessage) {
                    onMessage(JSON.parse(event.data));
                }
            };

            this.eventSource.onerror = async (event) => {
                this.eventSource.close();

                if (this.forcedClose) {
                    return;
                }

                if (this.retryCount < this.maxRetries) {
                    this.retryCount++;
                    try {
                        const newToken = await refreshSseToken();
                        this.url = new URL(`${BASE_URL}${this.endpoint}`);
                        this.url.searchParams.set('token', newToken);
                        setTimeout(() => this.connect(onMessage, onError), this.retryDelay); // Reconnect with delay
                    } catch (refreshError) {
                        if (onError) {
                            onError(refreshError);
                        }
                    }
                } else {
                    if (onError) {
                        onError(event);
                    }
                }
            };
        } catch (error) {
            if (this.retryCount < this.maxRetries) {
                this.retryCount++;
                try {
                    const newToken = await refreshSseToken();
                    this.url = new URL(`${BASE_URL}${this.endpoint}`);
                    this.url.searchParams.set('token', newToken);
                    setTimeout(() => this.connect(onMessage, onError), this.retryDelay); // Reconnect with delay
                } catch (refreshError) {
                    if (onError) {
                        onError(refreshError);
                    }
                }
            } else {
                if (onError) {
                    onError(error);
                }
            }
        }
    }

    disconnect() {
        if (this.eventSource) {
            this.forcedClose = true;
            this.eventSource.close();
        }
    }
}

export default SSEService;
