package cnr.isti.sse.big.util;

public class InfoTitoli {
	
	Integer quantita, corrispettivo, prevendita   = 0 ;
	Integer imponibileIntrattenimenti, incidenza  = 0;
	
	
	
	/**
	 * @param imponibileIntrattenimenti
	 * @param incidenza
	 */
	public InfoTitoli(Integer imponibileIntrattenimenti, Integer incidenza) {
		super();
		this.imponibileIntrattenimenti = imponibileIntrattenimenti;
		this.incidenza = incidenza;
	}
	/**
	 * @param quantita
	 * @param corrispettivo
	 * @param prevendita
	 * @param imponibileIntrattenimenti
	 * @param incidenza
	 */
	public InfoTitoli(Integer quantita, Integer corrispettivo, Integer prevendita, Integer imponibileIntrattenimenti,
			Integer incidenza) {
		super();
		this.quantita = quantita;
		this.corrispettivo = corrispettivo;
		this.prevendita = prevendita;
		this.imponibileIntrattenimenti = imponibileIntrattenimenti;
		this.incidenza = incidenza;
	}
	/**
	 * @param quantita
	 * @param corrispettivo
	 * @param prevendita
	 */
	public InfoTitoli(Integer quantita, Integer corrispettivo, Integer prevendita) {
		super();
		this.quantita = quantita;
		this.corrispettivo = corrispettivo;
		this.prevendita = prevendita;
	}
	public Integer getQuantita() {
		return quantita;
	}
	public void setQuantita(Integer quantita) {
		this.quantita = quantita;
	}
	public Integer getCorrispettivo() {
		return corrispettivo;
	}
	public void setCorrispettivo(Integer corrispettivo) {
		this.corrispettivo = corrispettivo;
	}
	public Integer getPrevendita() {
		return prevendita;
	}
	public void setPrevendita(Integer prevendita) {
		this.prevendita = prevendita;
	}
	public Integer getImponibileIntrattenimenti() {
		return imponibileIntrattenimenti;
	}
	public void setImponibileIntrattenimenti(Integer imponibileIntrattenimenti) {
		this.imponibileIntrattenimenti = imponibileIntrattenimenti;
	}
	public Integer getIncidenza() {
		return incidenza;
	}
	public void setIncidenza(Integer incidenza) {
		this.incidenza = incidenza;
	}
	@Override
	public String toString() {
		return (quantita != null ? "quantita: " + quantita + ", \\n " : "")
				+ (corrispettivo != null ? "corrispettivo: " + corrispettivo + ", \\n " : "")
				+ (prevendita != null ? "prevendita: " + prevendita + ", \\n " : "")
				+ (imponibileIntrattenimenti != null
						? "imponibileIntrattenimenti: " + imponibileIntrattenimenti + ", \\n "
						: "")
				+ (incidenza != null ? "incidenza: " + incidenza : "");
	}
	
	

}
