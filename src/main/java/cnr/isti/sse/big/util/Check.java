package cnr.isti.sse.big.util;

import cnr.isti.sse.big.data.transazioni.Transazione;

public class Check {
	public boolean codicefiscale(Transazione t ) {
		String cfo = t.getCFOrganizzatore();
		String cft = t.getCFTitolare();
		
		UCheckDigit ccfo = new UCheckDigit(cfo);
		boolean rcfo = ccfo.controllaCorrettezza();
		rcfo = rcfo & ccfo.controllaCheckDigit();
		UCheckDigit ccft = new UCheckDigit(cft);
		boolean rcft = ccft.controllaCorrettezza();
		rcft = rcft & ccft.controllaCheckDigit();
		if(rcft&rcfo) {
			return true;
		}
		
		return false;
	}
}
