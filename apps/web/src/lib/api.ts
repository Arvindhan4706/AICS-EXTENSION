const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api/v1';

export async function submitScan(url: string) {
    const response = await fetch(`${API_BASE_URL}/scans/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
    });

    if (!response.ok) {
        throw new Error('Failed to submit scan');
    }

    return response.json();
}

export async function getScanStatus(scanId: string) {
    const response = await fetch(`${API_BASE_URL}/scans/${scanId}`);

    if (!response.ok) {
        throw new Error('Failed to get scan status');
    }

    return response.json();
}
