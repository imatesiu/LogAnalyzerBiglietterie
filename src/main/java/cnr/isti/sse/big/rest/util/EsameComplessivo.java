package cnr.isti.sse.big.rest.util;

import java.util.ArrayList;
import java.util.List;

import org.apache.commons.lang3.tuple.ImmutableTriple;

import cnr.isti.sse.big.data.reply.accessi.RiepilogoControlloAccessi;
import cnr.isti.sse.big.data.reply.accessi.lta.LTAEvento;
import cnr.isti.sse.big.data.reply.accessi.lta.LTAGiornaliera;
import cnr.isti.sse.big.data.reply.rp.LogRP;
import cnr.isti.sse.big.data.riepilogogiornaliero.RiepilogoGiornaliero;
import cnr.isti.sse.big.data.riepilogomensile.Organizzatore;
import cnr.isti.sse.big.data.riepilogomensile.RiepilogoMensile;
import cnr.isti.sse.big.data.transazioni.LogTransazione;
import cnr.isti.sse.big.data.transazioni.Transazione;
import cnr.isti.sse.big.util.Utility;

public class EsameComplessivo {
	
	
	private static org.apache.logging.log4j.Logger log = org.apache.logging.log4j.LogManager.getLogger(EsameComplessivo.class);
	
	private List<LTAGiornaliera> lta;
	private List<RiepilogoControlloAccessi> rca;
	private List<RiepilogoGiornaliero> rpg;
	private RiepilogoMensile rpm;
	private List<LogTransazione> listlogtransazioni;
	
	public EsameComplessivo() {
		
	}

	
	
	public List<RiepilogoControlloAccessi> getRca() {
		if(rca==null) {
			rca = new ArrayList<RiepilogoControlloAccessi>();
		}
		return rca;
	}

	

	



	public List<LogTransazione> getListlogtransazioni() {
		if(listlogtransazioni==null) {
			listlogtransazioni = new ArrayList<>();
		}
		return listlogtransazioni;
	}



	public void setRca(List<RiepilogoControlloAccessi> rca) {
		this.rca = rca;
	}



	public List<RiepilogoGiornaliero> getRpg() {
		if(rpg==null) {
			rpg = new ArrayList<>();
		}
		return rpg;
	}



	public void setRpg(List<RiepilogoGiornaliero> rpg) {
		
		this.rpg = rpg;
	}



	public RiepilogoMensile getRpm() {
		if(rpm==null) {
			rpm = new RiepilogoMensile();
		}
		return rpm;
	}
	
	public List<LTAGiornaliera> getLta() {
		if(lta==null) {
			lta =  new ArrayList<LTAGiornaliera>();
		}
		return lta;
	}



	public void setRpm(RiepilogoMensile rpm) {
		this.rpm = rpm;
	}



	public void set(LTAGiornaliera logT) {
		if(this.lta==null) {
			this.lta = new ArrayList<LTAGiornaliera>();
		}
		this.lta.add(logT);
		
	}

	public void set(RiepilogoControlloAccessi logT) {
		if(this.rca==null) {
			this.rca = new ArrayList<RiepilogoControlloAccessi>();
		}
		this.rca.add(logT);
		
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
		log.info("***RPGs***");
		for(RiepilogoGiornaliero rp : this.getRpg() ) {
			List<Organizzatore> organizzatori = rp.getOrganizzatore();
			LogRP  l  =  Utility.check(organizzatori);
			f.update(l);
			
		}
		return f;
	}
	
	public void esame() {
		LogRP  lm = new LogRP();
		LogRP  lg = checkRPGs();
		if(rpm!=null) {
			List<Organizzatore> organizzatori = rpm.getOrganizzatore();
			log.info("***RPM***");
			lm  =  Utility.check(organizzatori);
			
			
			if(!lg.equals(lm)) {
				log.error("RPGs Diverso da RPM");
			}
			log.info("Dati complessivi del Mensile "+lm);
			log.info("Dati complessivi del Gionaliero "+lg);
		}
		
		ImmutableTriple<Integer, Integer, Integer> sum = checkLogs();
		log.info(sum);
		log.info(lm);
		log.info("***check RPM vs LOGTransazioni***");
		checkRPMtoLog(lm,sum);
		log.info("***check RPGs vs LOGTransazioni***");
		checkRPMtoLog(lg,sum);
		log.info("***check LTA***");
		checkLTA();
		log.info("***check RCA***");
		checkRCA();
		//log.info("ok");

	}
	private void checkRCA() {
		log.info(getRca());
		
	}



	private void checkRPMtoLog(LogRP lm, ImmutableTriple<Integer, Integer, Integer> sum) {
		ImmutableTriple<Integer, Integer, Integer> listsum = lm.sumAll();
		log.info(listsum);
		if(!listsum.equals(sum)) {
			log.error("*****Differenza tra Ripilogo e Log Transazioni");
		}else {
			log.info("Nessuna Differenza tra Ripilogo e Log Transazioni");
		}
	}

	private void checkLTA() {
		if(!this.getLta().isEmpty()) {
		List<Transazione>  ltransa = new ArrayList<Transazione>();
		for(LogTransazione logt : this.getListlogtransazioni()) {
			
			ltransa.addAll(logt.getTransazione());
		}
		List<cnr.isti.sse.big.data.reply.accessi.lta.TitoloAccesso> llta = new ArrayList<cnr.isti.sse.big.data.reply.accessi.lta.TitoloAccesso>();
		for(LTAGiornaliera ta :this.getLta()) {
			for( LTAEvento evento : ta.getLTAEvento()) {
				llta.addAll(evento.getTitoloAccesso());
			}
		}
		/*
		for( Transazione tr : ltransa) {
	       	 System.out.println(tr);
	       }*/
		log.info("*********** ******* titolinonpasatidagliaccessi * *************** *********");
		List<Transazione>  titolinonpasatidagliaccessi = new ArrayList<Transazione>();
		titolinonpasatidagliaccessi.addAll(ltransa);
		titolinonpasatidagliaccessi.removeAll(llta);

		log.info("Missing items from listTwo " + titolinonpasatidagliaccessi);
        for( Transazione tr : titolinonpasatidagliaccessi) {
        	log.info(tr);
        }
        log.info("*********** ******* passanoquellidellog * *************** *********");
		List<cnr.isti.sse.big.data.reply.accessi.lta.TitoloAccesso> passanoquellidellog = new ArrayList<cnr.isti.sse.big.data.reply.accessi.lta.TitoloAccesso>();
		passanoquellidellog.addAll(llta);
		passanoquellidellog.removeAll(ltransa);

		log.info("Missing items from listTwo2 " + passanoquellidellog);
        for( cnr.isti.sse.big.data.reply.accessi.lta.TitoloAccesso tr : passanoquellidellog) {
        	log.info(tr);
        }
		}
        
		
	}
	

	private ImmutableTriple<Integer, Integer, Integer> checkLogs() {
		List<ImmutableTriple<Integer, Integer, Integer>> limm = new ArrayList<ImmutableTriple<Integer,Integer,Integer>>();
		log.info("********CHECK LOGs********");
		for(LogTransazione logt : getListlogtransazioni()) {
			
			limm.add(Utility.check(logt));
		}
		ImmutableTriple<Integer, Integer, Integer> sum = Utility.sumImmutableTriple(limm);
		float totCorrispettivo = (float)sum.middle/100;
		log.info("Corrispettivo Lordo: "+ totCorrispettivo);
		float totPrevendita = (float)sum.right/100 ;
		log.info("Prevendita Lordo: "+ totPrevendita);
		float tot = (float)totCorrispettivo+totPrevendita;
		log.info("Totale Lordo: "+ tot);

		log.info("Totale Progressivi: "+ sum.left);
		return sum;
		
	}

}
