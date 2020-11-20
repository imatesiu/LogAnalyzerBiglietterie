package cnr.isti.sse.big.rest.util;

import java.util.ArrayList;
import java.util.List;

import org.apache.commons.lang3.tuple.ImmutableTriple;

import cnr.isti.sse.big.data.reply.accessi.RiepilogoControlloAccessi;
import cnr.isti.sse.big.data.reply.accessi.lta.LTAGiornaliera;
import cnr.isti.sse.big.data.reply.rp.LogRP;
import cnr.isti.sse.big.data.riepilogogiornaliero.RiepilogoGiornaliero;
import cnr.isti.sse.big.data.riepilogomensile.Organizzatore;
import cnr.isti.sse.big.data.riepilogomensile.RiepilogoMensile;
import cnr.isti.sse.big.data.transazioni.LogTransazione;
import cnr.isti.sse.big.util.Utility;

public class EsameComplessivo {
	
	
	private static org.apache.logging.log4j.Logger log = org.apache.logging.log4j.LogManager.getLogger(EsameComplessivo.class);
	
	private LTAGiornaliera lta;
	private RiepilogoControlloAccessi rca;
	private List<RiepilogoGiornaliero> rpg;
	private RiepilogoMensile rpm;
	private List<LogTransazione> listlogtransazioni;
	
	public EsameComplessivo() {
		
	}

	public void set(LTAGiornaliera logT) {
		this.lta = logT;
		
	}

	public void set(RiepilogoControlloAccessi logT) {
		this.rca = logT;
		
	}

	public void set(RiepilogoGiornaliero rPG) {
		if(rpg==null) {
			rpg = new ArrayList<RiepilogoGiornaliero>();
		}
		this.rpg.add(rPG);
		
	}

	public void set(RiepilogoMensile rPM) {
		this.rpm = rPM;
		
	}

	public void set(LogTransazione logT) {
		if(this.listlogtransazioni==null) {
			this.listlogtransazioni = new ArrayList<LogTransazione>();
		}
		this.listlogtransazioni.add(logT);
		
	}
	
	public LogRP checkRPGs() {
		LogRP f = new LogRP();
		for(RiepilogoGiornaliero rp :rpg) {
			List<Organizzatore> organizzatori = rp.getOrganizzatore();
			LogRP  l  =  Utility.check(organizzatori);
			f.update(l);
			
		}
		return f;
	}
	
	public void esame() {
		

		List<Organizzatore> organizzatori = rpm.getOrganizzatore();
		log.info("***RPM***");
		LogRP  lm  =  Utility.check(organizzatori);
		log.info("***RPGs***");
		LogRP lg = checkRPGs();
		if(!lg.equals(lm)) {
			log.error("RPGs Diverso da RPM");
		}
		log.info(lm);
		log.info(lg);
		checkLogs();
		
		
		//log.info("ok");
		
	}

	private void checkLogs() {
		List<ImmutableTriple<Integer, Integer, Integer>> limm = new ArrayList<ImmutableTriple<Integer,Integer,Integer>>();

		for(LogTransazione logt : listlogtransazioni) {
			
			limm.add(Utility.check(logt));
		}
		ImmutableTriple<Integer, Integer, Integer> sum = Utility.sumImmutableTriple(limm);
		
	}

}
