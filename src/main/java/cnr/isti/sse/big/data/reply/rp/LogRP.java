//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.11.18 alle 06:46:46 PM CET 
//


package cnr.isti.sse.big.data.reply.rp;

import java.math.BigInteger;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;

import org.apache.commons.lang3.tuple.ImmutableTriple;


/**
 * <p>Classe Java per anonymous complex type.
 * 
 * <p>Il seguente frammento di schema specifica il contenuto previsto contenuto in questa classe.
 * 
 * <pre>
 * &lt;complexType>
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="Abbonamenti">
 *           &lt;complexType>
 *             &lt;complexContent>
 *               &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *                 &lt;sequence>
 *                   &lt;element name="Vendite">
 *                     &lt;complexType>
 *                       &lt;complexContent>
 *                         &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *                           &lt;sequence>
 *                             &lt;element name="Quantita" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
 *                             &lt;element name="CorrispettivoLordo" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
 *                             &lt;element name="PrevenditaLordo" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
 *                           &lt;/sequence>
 *                         &lt;/restriction>
 *                       &lt;/complexContent>
 *                     &lt;/complexType>
 *                   &lt;/element>
 *                   &lt;element name="Annullati">
 *                     &lt;complexType>
 *                       &lt;complexContent>
 *                         &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *                           &lt;sequence>
 *                             &lt;element name="Quantita" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
 *                             &lt;element name="CorrispettivoLordo" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
 *                             &lt;element name="PrevenditaLordo" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
 *                           &lt;/sequence>
 *                         &lt;/restriction>
 *                       &lt;/complexContent>
 *                     &lt;/complexType>
 *                   &lt;/element>
 *                 &lt;/sequence>
 *               &lt;/restriction>
 *             &lt;/complexContent>
 *           &lt;/complexType>
 *         &lt;/element>
 *         &lt;element name="TitoliAccesso">
 *           &lt;complexType>
 *             &lt;complexContent>
 *               &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *                 &lt;sequence>
 *                   &lt;element name="Vendite">
 *                     &lt;complexType>
 *                       &lt;complexContent>
 *                         &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *                           &lt;sequence>
 *                             &lt;element name="Quantita" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
 *                             &lt;element name="CorrispettivoLordo" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
 *                             &lt;element name="PrevenditaLordo" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
 *                           &lt;/sequence>
 *                         &lt;/restriction>
 *                       &lt;/complexContent>
 *                     &lt;/complexType>
 *                   &lt;/element>
 *                   &lt;element name="Annullati">
 *                     &lt;complexType>
 *                       &lt;complexContent>
 *                         &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *                           &lt;sequence>
 *                             &lt;element name="Quantita" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
 *                             &lt;element name="CorrispettivoLordo" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
 *                             &lt;element name="PrevenditaLordo" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
 *                           &lt;/sequence>
 *                         &lt;/restriction>
 *                       &lt;/complexContent>
 *                     &lt;/complexType>
 *                   &lt;/element>
 *                 &lt;/sequence>
 *               &lt;/restriction>
 *             &lt;/complexContent>
 *           &lt;/complexType>
 *         &lt;/element>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "abbonamenti",
    "titoliAccesso"
})
@XmlRootElement(name = "LogRP")
public class LogRP {

    @XmlElement(name = "Abbonamenti", required = true)
    protected LogRP.Abbonamenti abbonamenti;
    @XmlElement(name = "TitoliAccesso", required = true)
    protected LogRP.TitoliAccesso titoliAccesso;
    
    public LogRP() {
    	
    }
    
    public LogRP(TitoliAccesso titoli, Abbonamenti abb) {
    	abbonamenti = abb;
    	titoliAccesso = titoli;
	}

	public void setTitoliA(ImmutableTriple<Integer, Integer, Integer> immv, ImmutableTriple<Integer, Integer, Integer> imma) {
    	titoliAccesso = new TitoliAccesso(immv,imma);
    	
    }

    /**
     * Recupera il valore della proprietà abbonamenti.
     * 
     * @return
     *     possible object is
     *     {@link LogRP.Abbonamenti }
     *     
     */
    public LogRP.Abbonamenti getAbbonamenti() {
        return abbonamenti;
    }

    /**
     * Imposta il valore della proprietà abbonamenti.
     * 
     * @param value
     *     allowed object is
     *     {@link LogRP.Abbonamenti }
     *     
     */
    public void setAbbonamenti(LogRP.Abbonamenti value) {
        this.abbonamenti = value;
    }

    /**
     * Recupera il valore della proprietà titoliAccesso.
     * 
     * @return
     *     possible object is
     *     {@link LogRP.TitoliAccesso }
     *     
     */
    public LogRP.TitoliAccesso getTitoliAccesso() {
        return titoliAccesso;
    }

    /**
     * Imposta il valore della proprietà titoliAccesso.
     * 
     * @param value
     *     allowed object is
     *     {@link LogRP.TitoliAccesso }
     *     
     */
    public void setTitoliAccesso(LogRP.TitoliAccesso value) {
        this.titoliAccesso = value;
    }


    /**
     * <p>Classe Java per anonymous complex type.
     * 
     * <p>Il seguente frammento di schema specifica il contenuto previsto contenuto in questa classe.
     * 
     * <pre>
     * &lt;complexType>
     *   &lt;complexContent>
     *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
     *       &lt;sequence>
     *         &lt;element name="Vendite">
     *           &lt;complexType>
     *             &lt;complexContent>
     *               &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
     *                 &lt;sequence>
     *                   &lt;element name="Quantita" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
     *                   &lt;element name="CorrispettivoLordo" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
     *                   &lt;element name="PrevenditaLordo" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
     *                 &lt;/sequence>
     *               &lt;/restriction>
     *             &lt;/complexContent>
     *           &lt;/complexType>
     *         &lt;/element>
     *         &lt;element name="Annullati">
     *           &lt;complexType>
     *             &lt;complexContent>
     *               &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
     *                 &lt;sequence>
     *                   &lt;element name="Quantita" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
     *                   &lt;element name="CorrispettivoLordo" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
     *                   &lt;element name="PrevenditaLordo" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
     *                 &lt;/sequence>
     *               &lt;/restriction>
     *             &lt;/complexContent>
     *           &lt;/complexType>
     *         &lt;/element>
     *       &lt;/sequence>
     *     &lt;/restriction>
     *   &lt;/complexContent>
     * &lt;/complexType>
     * </pre>
     * 
     * 
     */
    @XmlAccessorType(XmlAccessType.FIELD)
    @XmlType(name = "", propOrder = {
        "vendite",
        "annullati"
    })
    public static class Abbonamenti {

        @XmlElement(name = "Vendite", required = true)
        protected LogRP.Vendite vendite;
        @XmlElement(name = "Annullati", required = true)
        protected LogRP.Annullati annullati;
        
        
        public Abbonamenti(ImmutableTriple<Integer, Integer, Integer> immv, ImmutableTriple<Integer, Integer, Integer> imma) {
        	vendite = new Vendite(immv);
        	annullati = new Annullati(imma);
        }

        /**
         * Recupera il valore della proprietà vendite.
         * 
         * @return
         *     possible object is
         *     {@link LogRP.Vendite }
         *     
         */
        public LogRP.Vendite getVendite() {
            return vendite;
        }

        /**
         * Imposta il valore della proprietà vendite.
         * 
         * @param value
         *     allowed object is
         *     {@link LogRP.Vendite }
         *     
         */
        public void setVendite(LogRP.Vendite value) {
            this.vendite = value;
        }

        /**
         * Recupera il valore della proprietà annullati.
         * 
         * @return
         *     possible object is
         *     {@link LogRP.Annullati }
         *     
         */
        public LogRP.Annullati getAnnullati() {
            return annullati;
        }

        /**
         * Imposta il valore della proprietà annullati.
         * 
         * @param value
         *     allowed object is
         *     {@link LogRP.Annullati }
         *     
         */
        public void setAnnullati(LogRP.Annullati value) {
            this.annullati = value;
        }


       

    }


    /**
     * <p>Classe Java per anonymous complex type.
     * 
     * <p>Il seguente frammento di schema specifica il contenuto previsto contenuto in questa classe.
     * 
     * <pre>
     * &lt;complexType>
     *   &lt;complexContent>
     *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
     *       &lt;sequence>
     *         &lt;element name="Vendite">
     *           &lt;complexType>
     *             &lt;complexContent>
     *               &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
     *                 &lt;sequence>
     *                   &lt;element name="Quantita" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
     *                   &lt;element name="CorrispettivoLordo" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
     *                   &lt;element name="PrevenditaLordo" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
     *                 &lt;/sequence>
     *               &lt;/restriction>
     *             &lt;/complexContent>
     *           &lt;/complexType>
     *         &lt;/element>
     *         &lt;element name="Annullati">
     *           &lt;complexType>
     *             &lt;complexContent>
     *               &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
     *                 &lt;sequence>
     *                   &lt;element name="Quantita" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
     *                   &lt;element name="CorrispettivoLordo" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
     *                   &lt;element name="PrevenditaLordo" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
     *                 &lt;/sequence>
     *               &lt;/restriction>
     *             &lt;/complexContent>
     *           &lt;/complexType>
     *         &lt;/element>
     *       &lt;/sequence>
     *     &lt;/restriction>
     *   &lt;/complexContent>
     * &lt;/complexType>
     * </pre>
     * 
     * 
     */
    @XmlAccessorType(XmlAccessType.FIELD)
    @XmlType(name = "", propOrder = {
        "vendite",
        "annullati"
    })
    public static class TitoliAccesso {

        @XmlElement(name = "Vendite", required = true)
        protected LogRP.Vendite vendite;
        @XmlElement(name = "Annullati", required = true)
        protected LogRP.Annullati annullati;
        
        public TitoliAccesso(ImmutableTriple<Integer, Integer, Integer> immv, ImmutableTriple<Integer, Integer, Integer> imma) {
        	vendite = new Vendite(immv);
        	annullati = new Annullati(imma);
        }

        /**
         * Recupera il valore della proprietà vendite.
         * 
         * @return
         *     possible object is
         *     {@link LogRP.Vendite }
         *     
         */
        public LogRP.Vendite getVendite() {
            return vendite;
        }

        /**
         * Imposta il valore della proprietà vendite.
         * 
         * @param value
         *     allowed object is
         *     {@link LogRP.Vendite }
         *     
         */
        public void setVendite(LogRP.Vendite value) {
            this.vendite = value;
        }

        /**
         * Recupera il valore della proprietà annullati.
         * 
         * @return
         *     possible object is
         *     {@link LogRP.Annullati }
         *     
         */
        public LogRP.Annullati getAnnullati() {
            return annullati;
        }

        /**
         * Imposta il valore della proprietà annullati.
         * 
         * @param value
         *     allowed object is
         *     {@link LogRP.Annullati }
         *     
         */
        public void setAnnullati(LogRP.Annullati value) {
            this.annullati = value;
        }


        

    }
    /**
     * <p>Classe Java per anonymous complex type.
     * 
     * <p>Il seguente frammento di schema specifica il contenuto previsto contenuto in questa classe.
     * 
     * <pre>
     * &lt;complexType>
     *   &lt;complexContent>
     *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
     *       &lt;sequence>
     *         &lt;element name="Quantita" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
     *         &lt;element name="CorrispettivoLordo" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
     *         &lt;element name="PrevenditaLordo" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
     *       &lt;/sequence>
     *     &lt;/restriction>
     *   &lt;/complexContent>
     * &lt;/complexType>
     * </pre>
     * 
     * 
     */
    @XmlAccessorType(XmlAccessType.FIELD)
    @XmlType(name = "", propOrder = {
        "quantita",
        "corrispettivoLordo",
        "prevenditaLordo"
    })
    public static class Annullati {

        @XmlElement(name = "Quantita", required = true)
        protected BigInteger quantita;
        @XmlElement(name = "CorrispettivoLordo", required = true)
        protected BigInteger corrispettivoLordo;
        @XmlElement(name = "PrevenditaLordo", required = true)
        protected BigInteger prevenditaLordo;
        
        
        public Annullati (ImmutableTriple<Integer, Integer, Integer> imm){
        	quantita = BigInteger.valueOf(imm.left);
        	corrispettivoLordo  = BigInteger.valueOf(imm.middle);
        	prevenditaLordo  = BigInteger.valueOf(imm.right);
        }

        /**
         * Recupera il valore della proprietà quantita.
         * 
         * @return
         *     possible object is
         *     {@link BigInteger }
         *     
         */
        public BigInteger getQuantita() {
            return quantita;
        }

        /**
         * Imposta il valore della proprietà quantita.
         * 
         * @param value
         *     allowed object is
         *     {@link BigInteger }
         *     
         */
        public void setQuantita(BigInteger value) {
            this.quantita = value;
        }

        /**
         * Recupera il valore della proprietà corrispettivoLordo.
         * 
         * @return
         *     possible object is
         *     {@link BigInteger }
         *     
         */
        public BigInteger getCorrispettivoLordo() {
            return corrispettivoLordo;
        }

        /**
         * Imposta il valore della proprietà corrispettivoLordo.
         * 
         * @param value
         *     allowed object is
         *     {@link BigInteger }
         *     
         */
        public void setCorrispettivoLordo(BigInteger value) {
            this.corrispettivoLordo = value;
        }

        /**
         * Recupera il valore della proprietà prevenditaLordo.
         * 
         * @return
         *     possible object is
         *     {@link BigInteger }
         *     
         */
        public BigInteger getPrevenditaLordo() {
            return prevenditaLordo;
        }

        /**
         * Imposta il valore della proprietà prevenditaLordo.
         * 
         * @param value
         *     allowed object is
         *     {@link BigInteger }
         *     
         */
        public void setPrevenditaLordo(BigInteger value) {
            this.prevenditaLordo = value;
        }

		public ImmutableTriple<BigInteger, BigInteger, BigInteger>  all() {
			ImmutableTriple<BigInteger, BigInteger, BigInteger>  imm = new ImmutableTriple<BigInteger, BigInteger, BigInteger> (quantita,corrispettivoLordo,prevenditaLordo);
			return imm;
			
		}
		
		public void updateall(ImmutableTriple<BigInteger, BigInteger, BigInteger> immv) {
			quantita = quantita.add(immv.left);
        	corrispettivoLordo  = corrispettivoLordo.add(immv.middle);
        	prevenditaLordo  = prevenditaLordo.add(immv.right);
			
		}

    }


    /**
     * <p>Classe Java per anonymous complex type.
     * 
     * <p>Il seguente frammento di schema specifica il contenuto previsto contenuto in questa classe.
     * 
     * <pre>
     * &lt;complexType>
     *   &lt;complexContent>
     *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
     *       &lt;sequence>
     *         &lt;element name="Quantita" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
     *         &lt;element name="CorrispettivoLordo" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
     *         &lt;element name="PrevenditaLordo" type="{http://www.w3.org/2001/XMLSchema}BigInteger"/>
     *       &lt;/sequence>
     *     &lt;/restriction>
     *   &lt;/complexContent>
     * &lt;/complexType>
     * </pre>
     * 
     * 
     */
    @XmlAccessorType(XmlAccessType.FIELD)
    @XmlType(name = "", propOrder = {
        "quantita",
        "corrispettivoLordo",
        "prevenditaLordo"
    })
    public static class Vendite {

        @XmlElement(name = "Quantita", required = true)
        protected BigInteger quantita;
        @XmlElement(name = "CorrispettivoLordo", required = true)
        protected BigInteger corrispettivoLordo;
        @XmlElement(name = "PrevenditaLordo", required = true)
        protected BigInteger prevenditaLordo;
        
        public Vendite  (ImmutableTriple<Integer, Integer, Integer> imm){
        	quantita = BigInteger.valueOf(imm.left);
        	corrispettivoLordo  = BigInteger.valueOf(imm.middle);
        	prevenditaLordo  = BigInteger.valueOf(imm.right);
        }

        /**
         * Recupera il valore della proprietà quantita.
         * 
         * @return
         *     possible object is
         *     {@link BigInteger }
         *     
         */
        public BigInteger getQuantita() {
            return quantita;
        }

        /**
         * Imposta il valore della proprietà quantita.
         * 
         * @param value
         *     allowed object is
         *     {@link BigInteger }
         *     
         */
        public void setQuantita(BigInteger value) {
            this.quantita = value;
        }

        /**
         * Recupera il valore della proprietà corrispettivoLordo.
         * 
         * @return
         *     possible object is
         *     {@link BigInteger }
         *     
         */
        public BigInteger getCorrispettivoLordo() {
            return corrispettivoLordo;
        }

        /**
         * Imposta il valore della proprietà corrispettivoLordo.
         * 
         * @param value
         *     allowed object is
         *     {@link BigInteger }
         *     
         */
        public void setCorrispettivoLordo(BigInteger value) {
            this.corrispettivoLordo = value;
        }

        /**
         * Recupera il valore della proprietà prevenditaLordo.
         * 
         * @return
         *     possible object is
         *     {@link BigInteger }
         *     
         */
        public BigInteger getPrevenditaLordo() {
            return prevenditaLordo;
        }

        /**
         * Imposta il valore della proprietà prevenditaLordo.
         * 
         * @param value
         *     allowed object is
         *     {@link BigInteger }
         *     
         */
        public void setPrevenditaLordo(BigInteger value) {
            this.prevenditaLordo = value;
        }

		public ImmutableTriple<BigInteger, BigInteger, BigInteger>  all() {
			ImmutableTriple<BigInteger, BigInteger, BigInteger>  imm = new ImmutableTriple<BigInteger, BigInteger, BigInteger> (quantita,corrispettivoLordo,prevenditaLordo);
			return imm;
			
		}

		public void updateall(ImmutableTriple<BigInteger, BigInteger, BigInteger> immv) {
			quantita = quantita.add(immv.left);
        	corrispettivoLordo  = corrispettivoLordo.add(immv.middle);
        	prevenditaLordo  = prevenditaLordo.add(immv.right);
			
		}

    }


	public void update(LogRP l) {
		if(!(this.isEmpty() | l.isEmpty())) {
		ImmutableTriple<BigInteger, BigInteger, BigInteger>  immv = l.getTitoliAccesso().getVendite().all();
		ImmutableTriple<BigInteger, BigInteger, BigInteger>  imma = l.getTitoliAccesso().getAnnullati().all();
		this.getTitoliAccesso().getVendite().updateall(immv);
		this.getTitoliAccesso().getAnnullati().updateall(immv);
		
		
		ImmutableTriple<BigInteger, BigInteger, BigInteger>  immva = l.getAbbonamenti().getVendite().all();
		ImmutableTriple<BigInteger, BigInteger, BigInteger>  immaa = l.getAbbonamenti().getAnnullati().all();
		this.getAbbonamenti().getVendite().updateall(immva);
		this.getAbbonamenti().getAnnullati().updateall(immva);
		
		}else {
			this.setAbbonamenti(l.getAbbonamenti());
			this.setTitoliAccesso(l.getTitoliAccesso());
		}
	}

	private boolean isEmpty() {
		return this.titoliAccesso ==null;
	//	return false;
	}

}
