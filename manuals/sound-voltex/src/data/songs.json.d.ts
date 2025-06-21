export type Song = {
	identifier: string
	title: string
	artist: string
	groups: string[]
	charts: {
		NOV: number
		ADV: number
		EXH: number
		MXM?: number
		GRV?: number
		XCD?: number
		HVN?: number
		INF?: number
		VVD?: number
	}
}

declare const songs: Song[]
export default songs
