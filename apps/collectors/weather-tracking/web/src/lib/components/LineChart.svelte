<script>
	import Chart from 'chart.js/auto'
	import {onMount} from 'svelte'

	export let data, quants, range
	let canvas, chart, isMounted

	function getQuantValue(n, coords) {
		if (n === 0) return coords[0].y
		if (n === quants.length -1) return coords[coords.length - 1].y

		const quantRange = Math.round(range / quants)
		const coordsInRange = coords.filter(coords => coords.x > (n - 1) * quantRange && coords.x <= n * quantRange)
		return coordsInRange.map(c => c.y).reduce((p, c) => p + c, 0) / coordsInRange.length
	}

	$: (() => {
		if (!isMounted || !canvas || !data) return

		if (chart) chart.destroy()
		chart = new Chart(canvas.getContext('2d'), {
			type: 'line',
			data: ((d, q) => {
				console.log(q)
				const labels = []
				while (q--) labels.unshift(q)
				const datasets = Object.keys(d).map(location => {
					const data = []
					for (let i = 0; i < quants; i++) data.push(getQuantValue(i, d[location]))
					return {
						borderColor: `rgb(${Math.round(Math.random() * 255)}, ${Math.round(Math.random() * 255)}, ${Math.round(Math.random() * 255)})`,
						data,
						label: location,
					}
				})

				console.log(labels)
				return {
					datasets,
					labels
				}
			})(data, quants)
		})
	})()

	onMount(() => {
		isMounted = true
	})
</script>

<canvas bind:this={canvas} />