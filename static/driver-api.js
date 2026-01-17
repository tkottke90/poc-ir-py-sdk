/**
 * iRacing Driver API Poller
 * 
 * This module provides functions to poll the iRacing telemetry driver API
 * and handle the responses.
 */

/**
 * @typedef {Object} DriverData
 * @property {string} driver_name - The driver's full name
 * @property {string} driver_team - The team name
 * @property {string} driver_number - The car number
 * @property {string} driver_license - The license class and rating (e.g., "A 4.50")
 * @property {number} driver_irating - The driver's iRating
 * @property {number} driver_incidents - The driver's incident count for this session
 * @property {number} team_incidents - The team's total incident count
 * @property {number} driver_laps - Number of laps completed by the driver
 * @property {number} total_laps - Total laps in the race
 * @property {string} timestamp - ISO 8601 timestamp of when the data was captured
 */

/**
 * @typedef {Object} ApiError
 * @property {string} error - Error message from the API
 */

/**
 * Fetch driver data from the API
 * 
 * @param {string} host - The hostname (e.g., 'localhost' or '192.168.1.100')
 * @param {number} port - The port number (e.g., 9000)
 * @returns {Promise<DriverData>} The driver data object
 * @throws {Error} If the request fails or returns an error
 */
async function fetchDriverData(host, port) {
    const url = `http://${host}:${port}/api/driver`;
    
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            mode: 'cors'
        });
        
        if (!response.ok) {
            // Handle HTTP errors
            const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
            throw new Error(`HTTP ${response.status}: ${errorData.error || response.statusText}`);
        }
        
        const data = await response.json();
        
        // Check if the response contains an error field
        if (data.error) {
            throw new Error(data.error);
        }
        
        return data;
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            throw new Error(`Failed to connect to ${url}. Is the server running?`);
        }
        throw error;
    }
}

/**
 * Callback function for successful data retrieval
 * @callback OnDataCallback
 * @param {DriverData} data - The driver data received from the API
 * @returns {void}
 */

/**
 * Callback function for error handling
 * @callback OnErrorCallback
 * @param {Error} error - The error that occurred
 * @returns {void}
 */

/**
 * @typedef {Object} PollerControl
 * @property {() => void} stop - Stop the polling
 * @property {() => boolean} isRunning - Check if polling is active
 * @property {(newIntervalMs: number) => void} setInterval - Change the polling interval
 */

/**
 * Start polling the driver API at regular intervals
 * 
 * @param {string} host - The hostname
 * @param {number} port - The port number
 * @param {OnDataCallback} onData - Callback function called with driver data on success
 * @param {OnErrorCallback} onError - Callback function called with error on failure
 * @param {number} [intervalMs=1000] - Polling interval in milliseconds (default: 1000)
 * @returns {PollerControl} Object with methods to control the polling
 */
function startDriverPolling(host, port, onData, onError, intervalMs = 1000) {
    let intervalId = null;
    let isRunning = false;
    
    const poll = async () => {
        try {
            const data = await fetchDriverData(host, port);
            if (onData) {
                onData(data);
            }
        } catch (error) {
            if (onError) {
                onError(error);
            }
        }
    };
    
    // Start polling
    isRunning = true;
    poll(); // Call immediately
    intervalId = setInterval(poll, intervalMs);
    
    return {
        stop: () => {
            if (intervalId) {
                clearInterval(intervalId);
                intervalId = null;
                isRunning = false;
            }
        },
        
        isRunning: () => isRunning,
        
        setInterval: (newIntervalMs) => {
            if (intervalId) {
                clearInterval(intervalId);
                intervalId = setInterval(poll, newIntervalMs);
            }
        }
    };
}

/**
 * Callback function for getDriverData
 * @callback GetDriverDataCallback
 * @param {Error|null} error - Error object if request failed, null otherwise
 * @param {DriverData|null} data - Driver data if successful, null otherwise
 * @returns {void}
 */

/**
 * Fetch driver data once (no polling)
 * 
 * @param {string} host - The hostname
 * @param {number} port - The port number
 * @param {GetDriverDataCallback} callback - Callback function called with (error, data)
 * @returns {void}
 */
function getDriverData(host, port, callback) {
    fetchDriverData(host, port)
        .then(data => callback(null, data))
        .catch(error => callback(error, null));
}

// Export for use in Node.js or module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        fetchDriverData,
        startDriverPolling,
        getDriverData
    };
}

// Example usage with TypeScript-like intellisense:
/*
// Example 1: One-time fetch with full type information
fetchDriverData('localhost', 9000)
    .then(data => {
        // Your IDE will now show autocomplete for these properties:
        console.log('Driver:', data.driver_name);        // string
        console.log('Team:', data.driver_team);          // string
        console.log('Number:', data.driver_number);      // string
        console.log('License:', data.driver_license);    // string
        console.log('iRating:', data.driver_irating);    // number
        console.log('Incidents:', data.driver_incidents); // number
        console.log('Team Inc:', data.team_incidents);   // number
        console.log('Laps:', data.driver_laps);          // number
        console.log('Total:', data.total_laps);          // number
        console.log('Time:', data.timestamp);            // string (ISO 8601)
    })
    .catch(error => {
        console.error('Error:', error.message);
    });

// Example 2: Start polling with typed callbacks
const poller = startDriverPolling(
    'localhost',
    9000,
    (data) => {
        // data is typed as DriverData
        console.log(`${data.driver_name} (#${data.driver_number})`);
        console.log(`Lap ${data.driver_laps}/${data.total_laps}`);
        console.log(`Incidents: ${data.driver_incidents}`);
    },
    (error) => {
        // error is typed as Error
        console.error('Polling error:', error.message);
    },
    2000
);

// poller is typed as PollerControl
poller.stop();
console.log('Is running?', poller.isRunning());
poller.setInterval(5000);

// Example 3: Using callback style with types
getDriverData('localhost', 9000, (error, data) => {
    if (error) {
        // error is Error | null
        console.error('Error:', error.message);
        return;
    }
    // data is DriverData | null
    if (data) {
        console.log('Driver:', data.driver_name);
    }
});
*/