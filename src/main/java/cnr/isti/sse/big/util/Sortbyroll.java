package cnr.isti.sse.big.util;

import java.util.Comparator;

import cnr.isti.sse.big.data.transazioni.Transazione;

public class Sortbyroll implements Comparator<Transazione> 
{ 
    // Used for sorting in ascending order of 
    // roll number 
    public int compare(Transazione a, Transazione b) 
    { 
		return Integer.valueOf(a.getNumeroProgressivo()) - Integer.valueOf(b.getNumeroProgressivo());

    } 
} 