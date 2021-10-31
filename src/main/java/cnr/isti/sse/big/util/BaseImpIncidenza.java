package cnr.isti.sse.big.util;

public class BaseImpIncidenza {
	
	double baseimposta, baseimpiva = 0;
	
	

	@Override
	public String toString() {
		return "baseimposta: " + baseimposta + ", \\n baseimpiva: " + baseimpiva;
	}

	/**
	 * @param baseimposta
	 * @param baseimpiva
	 */
	public BaseImpIncidenza(double baseimposta, double baseimpiva) {
		super();
		this.baseimposta = baseimposta;
		this.baseimpiva = baseimpiva;
	}

	public double getBaseimposta() {
		return baseimposta;
	}

	public void setBaseimposta(double baseimposta) {
		this.baseimposta = baseimposta;
	}

	public double getBaseimpiva() {
		return baseimpiva;
	}

	public void setBaseimpiva(double baseimpiva) {
		this.baseimpiva = baseimpiva;
	}
	
	

}
