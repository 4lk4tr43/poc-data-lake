<script>
	import {onMount} from 'svelte'
	import LineChart from '$lib/components/LineChart.svelte'

	function toDateTimeLocal(now) {
		now.setMinutes(now.getMinutes() - now.getTimezoneOffset())
		return now.toISOString().slice(0, 16)
	}

	let isMounted
	let start = toDateTimeLocal(
		(() => {
			const d = new Date()
			d.setHours(d.getHours() - 1)
			return d
		})(),
	)
	let end = toDateTimeLocal(new Date())

	let data
	$: (async () => {
		if (!isMounted || !start || !end) return

		const url = `/api/get-measures/${new Date(start).getTime()}/${new Date(end).getTime()}`
		const records = await (await fetch(url)).json()

		const dataByLocation = records.reduce((p, c) => {
			p[c.location] = [
				...(p[c.location] || []),
				{x: new Date(c.created_at).getTime(), y: c.temperature},
			]
			return p
		}, {})
		Object.keys(dataByLocation).forEach(location => {
			const xCoords = dataByLocation[location].map((coords) => coords.x)
			const minX = Math.min(...xCoords)
			dataByLocation[location] = dataByLocation[location].map(({x, y}) => {
				return {x: x - minX, y}
			})
		})

		data = dataByLocation
	})()

	onMount(() => {
		isMounted = true
	})
</script>

<label>
	Start Time
	<input bind:value={start} type="datetime-local"/>
</label>

<label>
	End Time
	<input bind:value={end} type="datetime-local"/>
</label>

<hr>

{#if data}
	<LineChart {data} quants="10" range={new Date(end).getTime() - new Date(start).getTime()}/>
{/if}

<hr>

<style>
	label {
		background: black;
		color: whitesmoke;
		display: block;
		font-weight: bolder;
		padding: 1rem;
		width: 16rem;
	}

	input {
		margin-top: 0.5rem;
		width: 100%;
	}
</style>
