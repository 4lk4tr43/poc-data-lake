import MariaDB from 'mariadb'

export async function get({params}) {
    const response = {}

    if (!params.start || !params.end) {
        response.status = 400
        return response
    }

    const pool = MariaDB.createPool({
        host: 'weather_tracking-db',
        user: 'root',
        connectionLimit: 5,
    })

    const start = new Date(parseInt(params.start))
        .toISOString()
        .replace(/T/, ' ')
        .replace(/\..*/, '')
    const end = new Date(parseInt(params.end))
        .toISOString()
        .replace(/T/, ' ')
        .replace(/\..*/, '')

    const connection = await pool.getConnection()
    const result = await connection.query(
        'SELECT * from `weather-tracking`.measures WHERE created_at BETWEEN (?) AND (?)',
        [start, end],
    )
    connection.end().then(() => {
    })

    return {body: JSON.stringify(result)}
}