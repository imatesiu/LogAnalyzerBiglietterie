//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.11.18 alle 06:46:46 PM CET 
//


package cnr.isti.sse.big.data.reply.rp;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;

import org.apache.commons.lang3.tuple.ImmutableTriple;

import cnr.isti.sse.big.util.Utility;


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
    "titoliAccesso",
    "bigliettiAbbonamenti"
})
@XmlRootElement(name = "LogRP")
public class LogRP {

    @XmlElement(name = "Abbonamenti", required = true)
    protected LogRP.Abbonamenti abbonamenti;
    @XmlElement(name = "BigliettiAbbonamenti", required = true)
    protected LogRP.BigliettiAbbonamenti bigliettiabbonamenti;
    @XmlElement(name = "TitoliAccesso", required = true)
    protected LogRP.TitoliAccesso titoliAccesso;
    
    public LogRP() {
    	
    }
    
    
	private static org.apache.logging.log4j.Logger log = org.apache.logging.log4j.LogManager.getLogger(LogRP.class);



	@Override
	public boolean equals(Object obj) {
		if (this == obj) {
			return true;
		}
		if (!(obj instanceof LogRP)) {
			return false;
		}
		LogRP other = (LogRP) obj;
		if (abbonamenti == null) {
			if (other.abbonamenti != null) {
				return false;
			}
		} else if (!abbonamenti.equals(other.abbonamenti)) {
			return false;
		}
		if (titoliAccesso == null) {
			if (other.titoliAccesso != null) {
				return false;
			}
		} else if (!titoliAccesso.equals(other.titoliAccesso)) {
			return false;
		}
		return true;
	}
	
	

	

	public LogRP.BigliettiAbbonamenti getBigliettiabbonamenti() {
		if(bigliettiabbonamenti==null)
			bigliettiabbonamenti= new LogRP.BigliettiAbbonamenti();
		return bigliettiabbonamenti;
	}





	public void setBigliettiabbonamenti(LogRP.BigliettiAbbonamenti bigliettiabbonamenti) {
		this.bigliettiabbonamenti = bigliettiabbonamenti;
	}





	public LogRP(TitoliAccesso titoli, Abbonamenti abb, BigliettiAbbonamenti babb) {
    	abbonamenti = abb;
    	titoliAccesso = titoli;
    	bigliettiabbonamenti = babb;
	}

	public void setTitoliA(ImmutableTriple<Integer, Integer, Integer> immv, ImmutableTriple<Integer, Integer, Integer> imma) {
    	titoliAccesso = new TitoliAccesso(immv,imma);
    	
    }
	
	public ImmutableTriple<Integer, Integer, Integer> sumVendite(){
		List<ImmutableTriple<BigInteger, BigInteger, BigInteger>> lsum = new ArrayList<ImmutableTriple<BigInteger, BigInteger, BigInteger>>();
		lsum.add(this.getAbbonamenti().getVendite().all());
		lsum.add(this.getBigliettiabbonamenti().getVendite().onlyQ());
		lsum.add(this.getTitoliAccesso().getVendite().all());
		
		//numerotitoliiva, corrispettivo, prevendita
		return Utility.sumImmutableTripleBig(lsum);
	}
	
	public ImmutableTriple<Integer, Integer, Integer> sumAnnulli(){
		List<ImmutableTriple<BigInteger, BigInteger, BigInteger>> lsum = new ArrayList<ImmutableTriple<BigInteger, BigInteger, BigInteger>>();
			lsum.add(this.getAbbonamenti().getAnnullati().all());
			lsum.add(this.getBigliettiabbonamenti().getAnnullati().onlyQ());

			lsum.add(this.getTitoliAccesso().getAnnullati().all());
			
			//numerotitoliiva, corrispettivo, prevendita
			return Utility.sumImmutableTripleBig(lsum);
	}
	
	public ImmutableTriple<Integer, Integer, Integer> sumAll(){
		List<ImmutableTriple<Integer, Integer, Integer>> lsum = new ArrayList<ImmutableTriple<Integer, Integer, Integer>>();
			lsum.add(this.sumVendite());
			lsum.add(this.sumAnnulli());
			
			//numerotitoliiva, corrispettivo, prevendita
			return Utility.sumImmutableTriple(lsum);
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
    	if(abbonamenti==null)
    		abbonamenti= new Abbonamenti();
    		
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
    	if(titoliAccesso==null)
    		titoliAccesso= new TitoliAccesso();
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

    
    
    @Override
	public String toString() {
		return (abbonamenti != null ? "abbonamenti: " + abbonamenti + ",  " : "")
				+ (titoliAccesso != null ? "titoliAccesso: " + titoliAccesso : "");
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

        public Abbonamenti() {
        	vendite = new Vendite();
        	annullati = new Annullati();
        }
        
       



		@Override
		public boolean equals(Object obj) {
			if (this == obj) {
				return true;
			}
			if (!(obj instanceof Abbonamenti)) {
				return false;
			}
			Abbonamenti other = (Abbonamenti) obj;
			if (annullati == null) {
				if (other.annullati != null) {
					return false;
				}
			} else if (!annullati.equals(other.annullati)) {
				log.info("diff Abbonamenti annullati");
				return false;
			}
			if (vendite == null) {
				if (other.vendite != null) {
					return false;
				}
			} else if (!vendite.equals(other.vendite)) {
				log.info("diff Abbonamenti vendite");
				return false;
			}
			return true;
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

		@Override
		public String toString() {
			return (vendite != null ? "vendite: " + vendite + ",  " : "")
					+ (annullati != null ? "annullati: " + annullati : "");
		}

        
       

    }

    @XmlAccessorType(XmlAccessType.FIELD)
    @XmlType(name = "", propOrder = {
        "vendite",
        "annullati"
    })
    public static class BigliettiAbbonamenti {

        @XmlElement(name = "Vendite", required = true)
        protected LogRP.Vendite vendite;
        @XmlElement(name = "Annullati", required = true)
        protected LogRP.Annullati annullati;
        
        
        public BigliettiAbbonamenti(ImmutableTriple<Integer, Integer, Integer> immv, ImmutableTriple<Integer, Integer, Integer> imma) {
        	vendite = new Vendite(immv);
        	annullati = new Annullati(imma);
        }

        public BigliettiAbbonamenti() {
        	vendite = new Vendite();
        	annullati = new Annullati();
        }
        
       



		@Override
		public boolean equals(Object obj) {
			if (this == obj) {
				return true;
			}
			if (!(obj instanceof BigliettiAbbonamenti)) {
				return false;
			}
			BigliettiAbbonamenti other = (BigliettiAbbonamenti) obj;
			if (annullati == null) {
				if (other.annullati != null) {
					return false;
				}
			} else if (!annullati.equals(other.annullati)) {
				log.info("diff BigliettiAbbonamenti annullati");
				return false;
			}
			if (vendite == null) {
				if (other.vendite != null) {
					return false;
				}
			} else if (!vendite.equals(other.vendite)) {
				log.info("diff BigliettiAbbonamenti Emissione");
				return false;
			}
			return true;
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

		@Override
		public String toString() {
			return (vendite != null ? "vendite: " + vendite + ",  " : "")
					+ (annullati != null ? "annullati: " + annullati : "");
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
        

        @Override
		public String toString() {
			return (vendite != null ? "vendite: " + vendite + ",  " : "")
					+ (annullati != null ? "annullati: " + annullati : "");
		}
        

        public TitoliAccesso() {
        	vendite = new Vendite();
        	annullati = new Annullati();
        }

		@Override
		public boolean equals(Object obj) {
			if (this == obj) {
				return true;
			}
			if (!(obj instanceof TitoliAccesso)) {
				return false;
			}
			TitoliAccesso other = (TitoliAccesso) obj;
			if (annullati == null) {
				if (other.annullati != null) {
					return false;
				}
			} else if (!annullati.equals(other.annullati)) {
				log.info("diff TitoliAccesso annullati");
				return false;
			}
			if (vendite == null) {
				if (other.vendite != null) {
					return false;
				}
			} else if (!vendite.equals(other.vendite)) {
				log.info("diff TitoliAccesso vendite");
				return false;
			}
			return true;
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
        protected BigInteger quantita = BigInteger.ZERO;
        @XmlElement(name = "CorrispettivoLordo", required = true)
        protected BigInteger corrispettivoLordo  = BigInteger.ZERO;
        @XmlElement(name = "PrevenditaLordo", required = true)
        protected BigInteger prevenditaLordo = BigInteger.ZERO;
        
        
        public Annullati (ImmutableTriple<Integer, Integer, Integer> imm){
        	quantita = BigInteger.valueOf(imm.left);
        	corrispettivoLordo  = BigInteger.valueOf(imm.middle);
        	prevenditaLordo  = BigInteger.valueOf(imm.right);
        }
        
        public ImmutableTriple<BigInteger, BigInteger, BigInteger> onlyQ() {
			// TODO Auto-generated method stub
			ImmutableTriple<BigInteger, BigInteger, BigInteger>  imm = new ImmutableTriple<BigInteger, BigInteger, BigInteger> (quantita,BigInteger.ZERO,BigInteger.ZERO);
			return imm;
		}

		public Annullati() {
			// TODO Auto-generated constructor stub
		}

		@Override
		public boolean equals(Object obj) {
			if (this == obj) {
				return true;
			}
			if (!(obj instanceof Annullati)) {
				return false;
			}
			Annullati other = (Annullati) obj;
			if (corrispettivoLordo == null) {
				if (other.corrispettivoLordo != null) {
					return false;
				}
			} else if (!corrispettivoLordo.equals(other.corrispettivoLordo)) {
				log.info("diff corrispettivoLordo");
				return false;
			}
			if (prevenditaLordo == null) {
				if (other.prevenditaLordo != null) {
					return false;
				}
			} else if (!prevenditaLordo.equals(other.prevenditaLordo)) {
				log.info("diff prevenditaLordo");

				return false;
			}
			if (quantita == null) {
				if (other.quantita != null) {
					return false;
				}
			} else if (!quantita.equals(other.quantita)) {
				log.info("diff quantita");

				return false;
			}
			return true;
		}
        
        @Override
		public String toString() {
			return (quantita != null ? "quantita: " + quantita + ",  " : "")
					+ (corrispettivoLordo != null ? "corrispettivoLordo: " + corrispettivoLordo + ",  " : "")
					+ (prevenditaLordo != null ? "prevenditaLordo: " + prevenditaLordo : "");
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
        protected BigInteger quantita = BigInteger.ZERO;
        @XmlElement(name = "CorrispettivoLordo", required = true)
        protected BigInteger corrispettivoLordo = BigInteger.ZERO ;
        @XmlElement(name = "PrevenditaLordo", required = true)
        protected BigInteger prevenditaLordo = BigInteger.ZERO;
        
        public Vendite  (ImmutableTriple<Integer, Integer, Integer> imm){
        	quantita = BigInteger.valueOf(imm.left);
        	corrispettivoLordo  = BigInteger.valueOf(imm.middle);
        	prevenditaLordo  = BigInteger.valueOf(imm.right);
        }

        
      

		public ImmutableTriple<BigInteger, BigInteger, BigInteger> onlyQ() {
			// TODO Auto-generated method stub
			ImmutableTriple<BigInteger, BigInteger, BigInteger>  imm = new ImmutableTriple<BigInteger, BigInteger, BigInteger> (quantita,BigInteger.ZERO,BigInteger.ZERO);
			return imm;
		}




		public Vendite() {
			// TODO Auto-generated constructor stub
		}

		


		@Override
		public boolean equals(Object obj) {
			if (this == obj) {
				return true;
			}
			if (!(obj instanceof Vendite)) {
				return false;
			}
			Vendite other = (Vendite) obj;
			if (corrispettivoLordo == null) {
				if (other.corrispettivoLordo != null) {
					return false;
				}
			} else if (!corrispettivoLordo.equals(other.corrispettivoLordo)) {
				log.info("diff corrispettivoLordo");
				return false;
			}
			if (prevenditaLordo == null) {
				if (other.prevenditaLordo != null) {
					return false;
				}
			} else if (!prevenditaLordo.equals(other.prevenditaLordo)) {
				log.info("diff prevenditaLordo");
				return false;
			}
			if (quantita == null) {
				if (other.quantita != null) {
					return false;
				}
			} else if (!quantita.equals(other.quantita)) {
				log.info("diff quantita");
				return false;
			}
			return true;
		}
		

		@Override
		public String toString() {
			return (quantita != null ? "quantita: " + quantita + ",  " : "")
					+ (corrispettivoLordo != null ? "corrispettivoLordo: " + corrispettivoLordo + ",  " : "")
					+ (prevenditaLordo != null ? "prevenditaLordo: " + prevenditaLordo : "");
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
		this.getTitoliAccesso().getAnnullati().updateall(imma);
		
		
		ImmutableTriple<BigInteger, BigInteger, BigInteger>  immva = l.getAbbonamenti().getVendite().all();
		ImmutableTriple<BigInteger, BigInteger, BigInteger>  immaa = l.getAbbonamenti().getAnnullati().all();
		this.getAbbonamenti().getVendite().updateall(immva);
		this.getAbbonamenti().getAnnullati().updateall(immaa);
		
		ImmutableTriple<BigInteger, BigInteger, BigInteger>  immvba = l.getBigliettiabbonamenti().getVendite().all();
		ImmutableTriple<BigInteger, BigInteger, BigInteger>  immaba = l.getBigliettiabbonamenti().getAnnullati().all();
		//this.getBigliettiabbonamenti().getVendite().updateall(immvba);
		//this.getBigliettiabbonamenti().getAnnullati().updateall(immaba);
		
		}else {
			this.setAbbonamenti(l.getAbbonamenti());
			this.setBigliettiabbonamenti(l.getBigliettiabbonamenti());
			this.setTitoliAccesso(l.getTitoliAccesso());
		}
	}

	private boolean isEmpty() {
		return this.titoliAccesso ==null;
	//	return false;
	}

}
