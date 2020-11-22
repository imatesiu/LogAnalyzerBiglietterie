//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.11.18 alle 10:56:34 PM CET 
//


package cnr.isti.sse.big.data.reply.accessi.lta;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.adapters.CollapsedStringAdapter;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;


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
 *         &lt;element ref="{http://tempuri.org/lta}Partecipante" minOccurs="0"/>
 *       &lt;/sequence>
 *       &lt;attribute name="SistemaEmissione" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CartaAttivazione" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="ProgressivoFiscale" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="SigilloFiscale" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="DataEmissione" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="OraEmissione" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="DataLTA" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="OraLTA" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="TipoTitolo" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CodiceOrdine" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CorrispettivoLordo" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="Posto" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="Abbonamento" default="N">
 *         &lt;simpleType>
 *           &lt;restriction base="{http://www.w3.org/2001/XMLSchema}NMTOKEN">
 *             &lt;enumeration value="S"/>
 *             &lt;enumeration value="N"/>
 *           &lt;/restriction>
 *         &lt;/simpleType>
 *       &lt;/attribute>
 *       &lt;attribute name="CFAbbonamento" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CodiceAbbonamento" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="ProgressivoAbbonamento" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="QEventiAbilitati" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="Annullamento" default="N">
 *         &lt;simpleType>
 *           &lt;restriction base="{http://www.w3.org/2001/XMLSchema}NMTOKEN">
 *             &lt;enumeration value="S"/>
 *             &lt;enumeration value="N"/>
 *           &lt;/restriction>
 *         &lt;/simpleType>
 *       &lt;/attribute>
 *       &lt;attribute name="DataANN" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="OraANN" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CartaAttivazioneANN" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="ProgressivoFiscaleANN" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="SigilloFiscaleANN" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CodSupporto" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="IdSupporto" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="IdSupAlt" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="Stato" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="DataIngresso" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="OraIngresso" type="{http://www.w3.org/2001/XMLSchema}string" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "partecipante"
})
@XmlRootElement(name = "TitoloAccesso")
public class TitoloAccesso {

    @XmlElement(name = "Partecipante")
    protected Partecipante partecipante;
    @XmlAttribute(name = "SistemaEmissione", required = true)
    protected String sistemaEmissione;
    @XmlAttribute(name = "CartaAttivazione", required = true)
    protected String cartaAttivazione;
    @XmlAttribute(name = "ProgressivoFiscale", required = true)
    protected String progressivoFiscale;
    @XmlAttribute(name = "SigilloFiscale", required = true)
    protected String sigilloFiscale;
    @XmlAttribute(name = "DataEmissione", required = true)
    protected String dataEmissione;
    @XmlAttribute(name = "OraEmissione", required = true)
    protected String oraEmissione;
    @XmlAttribute(name = "DataLTA", required = true)
    protected String dataLTA;
    @XmlAttribute(name = "OraLTA", required = true)
    protected String oraLTA;
    @XmlAttribute(name = "TipoTitolo", required = true)
    protected String tipoTitolo;
    @XmlAttribute(name = "CodiceOrdine", required = true)
    protected String codiceOrdine;
    @XmlAttribute(name = "CorrispettivoLordo", required = true)
    protected String corrispettivoLordo;
    @XmlAttribute(name = "Posto")
    protected String posto;
    @XmlAttribute(name = "Abbonamento")
    @XmlJavaTypeAdapter(CollapsedStringAdapter.class)
    protected String abbonamento;
    @XmlAttribute(name = "CFAbbonamento")
    protected String cfAbbonamento;
    @XmlAttribute(name = "CodiceAbbonamento")
    protected String codiceAbbonamento;
    @XmlAttribute(name = "ProgressivoAbbonamento")
    protected String progressivoAbbonamento;
    @XmlAttribute(name = "QEventiAbilitati")
    protected String qEventiAbilitati;
    @XmlAttribute(name = "Annullamento")
    @XmlJavaTypeAdapter(CollapsedStringAdapter.class)
    protected String annullamento;
    @XmlAttribute(name = "DataANN")
    protected String dataANN;
    @XmlAttribute(name = "OraANN")
    protected String oraANN;
    @XmlAttribute(name = "CartaAttivazioneANN")
    protected String cartaAttivazioneANN;
    @XmlAttribute(name = "ProgressivoFiscaleANN")
    protected String progressivoFiscaleANN;
    @XmlAttribute(name = "SigilloFiscaleANN")
    protected String sigilloFiscaleANN;
    @XmlAttribute(name = "CodSupporto", required = true)
    protected String codSupporto;
    @XmlAttribute(name = "IdSupporto", required = true)
    protected String idSupporto;
    @XmlAttribute(name = "IdSupAlt")
    protected String idSupAlt;
    @XmlAttribute(name = "Stato", required = true)
    protected String stato;
    @XmlAttribute(name = "DataIngresso")
    protected String dataIngresso;
    @XmlAttribute(name = "OraIngresso")
    protected String oraIngresso;

    /**
     * Recupera il valore della proprietà partecipante.
     * 
     * @return
     *     possible object is
     *     {@link Partecipante }
     *     
     */
    public Partecipante getPartecipante() {
        return partecipante;
    }

    /**
     * Imposta il valore della proprietà partecipante.
     * 
     * @param value
     *     allowed object is
     *     {@link Partecipante }
     *     
     */
    public void setPartecipante(Partecipante value) {
        this.partecipante = value;
    }

    /**
     * Recupera il valore della proprietà sistemaEmissione.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getSistemaEmissione() {
        return sistemaEmissione;
    }

    /**
     * Imposta il valore della proprietà sistemaEmissione.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSistemaEmissione(String value) {
        this.sistemaEmissione = value;
    }

    /**
     * Recupera il valore della proprietà cartaAttivazione.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCartaAttivazione() {
        return cartaAttivazione;
    }

    /**
     * Imposta il valore della proprietà cartaAttivazione.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCartaAttivazione(String value) {
        this.cartaAttivazione = value;
    }

    /**
     * Recupera il valore della proprietà progressivoFiscale.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getProgressivoFiscale() {
        return progressivoFiscale;
    }

    /**
     * Imposta il valore della proprietà progressivoFiscale.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setProgressivoFiscale(String value) {
        this.progressivoFiscale = value;
    }

    /**
     * Recupera il valore della proprietà sigilloFiscale.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getSigilloFiscale() {
        return sigilloFiscale;
    }

    /**
     * Imposta il valore della proprietà sigilloFiscale.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSigilloFiscale(String value) {
        this.sigilloFiscale = value;
    }

    /**
     * Recupera il valore della proprietà dataEmissione.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDataEmissione() {
        return dataEmissione;
    }

    /**
     * Imposta il valore della proprietà dataEmissione.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDataEmissione(String value) {
        this.dataEmissione = value;
    }

    /**
     * Recupera il valore della proprietà oraEmissione.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getOraEmissione() {
        return oraEmissione;
    }

    /**
     * Imposta il valore della proprietà oraEmissione.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setOraEmissione(String value) {
        this.oraEmissione = value;
    }

    /**
     * Recupera il valore della proprietà dataLTA.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDataLTA() {
        return dataLTA;
    }

    /**
     * Imposta il valore della proprietà dataLTA.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDataLTA(String value) {
        this.dataLTA = value;
    }

    /**
     * Recupera il valore della proprietà oraLTA.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getOraLTA() {
        return oraLTA;
    }

    /**
     * Imposta il valore della proprietà oraLTA.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setOraLTA(String value) {
        this.oraLTA = value;
    }

    /**
     * Recupera il valore della proprietà tipoTitolo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTipoTitolo() {
        return tipoTitolo;
    }

    /**
     * Imposta il valore della proprietà tipoTitolo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTipoTitolo(String value) {
        this.tipoTitolo = value;
    }

    /**
     * Recupera il valore della proprietà codiceOrdine.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCodiceOrdine() {
        return codiceOrdine;
    }

    /**
     * Imposta il valore della proprietà codiceOrdine.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCodiceOrdine(String value) {
        this.codiceOrdine = value;
    }

    /**
     * Recupera il valore della proprietà corrispettivoLordo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCorrispettivoLordo() {
        return corrispettivoLordo;
    }

    /**
     * Imposta il valore della proprietà corrispettivoLordo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCorrispettivoLordo(String value) {
        this.corrispettivoLordo = value;
    }

    /**
     * Recupera il valore della proprietà posto.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getPosto() {
        return posto;
    }

    /**
     * Imposta il valore della proprietà posto.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setPosto(String value) {
        this.posto = value;
    }

    /**
     * Recupera il valore della proprietà abbonamento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getAbbonamento() {
        if (abbonamento == null) {
            return "N";
        } else {
            return abbonamento;
        }
    }

    /**
     * Imposta il valore della proprietà abbonamento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setAbbonamento(String value) {
        this.abbonamento = value;
    }

    /**
     * Recupera il valore della proprietà cfAbbonamento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCFAbbonamento() {
        return cfAbbonamento;
    }

    /**
     * Imposta il valore della proprietà cfAbbonamento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCFAbbonamento(String value) {
        this.cfAbbonamento = value;
    }

    /**
     * Recupera il valore della proprietà codiceAbbonamento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCodiceAbbonamento() {
        return codiceAbbonamento;
    }

    /**
     * Imposta il valore della proprietà codiceAbbonamento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCodiceAbbonamento(String value) {
        this.codiceAbbonamento = value;
    }

    /**
     * Recupera il valore della proprietà progressivoAbbonamento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getProgressivoAbbonamento() {
        return progressivoAbbonamento;
    }

    /**
     * Imposta il valore della proprietà progressivoAbbonamento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setProgressivoAbbonamento(String value) {
        this.progressivoAbbonamento = value;
    }

    /**
     * Recupera il valore della proprietà qEventiAbilitati.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getQEventiAbilitati() {
        return qEventiAbilitati;
    }

    /**
     * Imposta il valore della proprietà qEventiAbilitati.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setQEventiAbilitati(String value) {
        this.qEventiAbilitati = value;
    }

    /**
     * Recupera il valore della proprietà annullamento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getAnnullamento() {
        if (annullamento == null) {
            return "N";
        } else {
            return annullamento;
        }
    }

    /**
     * Imposta il valore della proprietà annullamento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setAnnullamento(String value) {
        this.annullamento = value;
    }

    /**
     * Recupera il valore della proprietà dataANN.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDataANN() {
        return dataANN;
    }

    /**
     * Imposta il valore della proprietà dataANN.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDataANN(String value) {
        this.dataANN = value;
    }

    /**
     * Recupera il valore della proprietà oraANN.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getOraANN() {
        return oraANN;
    }

    /**
     * Imposta il valore della proprietà oraANN.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setOraANN(String value) {
        this.oraANN = value;
    }

    /**
     * Recupera il valore della proprietà cartaAttivazioneANN.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCartaAttivazioneANN() {
        return cartaAttivazioneANN;
    }

    /**
     * Imposta il valore della proprietà cartaAttivazioneANN.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCartaAttivazioneANN(String value) {
        this.cartaAttivazioneANN = value;
    }

    /**
     * Recupera il valore della proprietà progressivoFiscaleANN.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getProgressivoFiscaleANN() {
        return progressivoFiscaleANN;
    }

    /**
     * Imposta il valore della proprietà progressivoFiscaleANN.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setProgressivoFiscaleANN(String value) {
        this.progressivoFiscaleANN = value;
    }

    /**
     * Recupera il valore della proprietà sigilloFiscaleANN.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getSigilloFiscaleANN() {
        return sigilloFiscaleANN;
    }

    /**
     * Imposta il valore della proprietà sigilloFiscaleANN.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSigilloFiscaleANN(String value) {
        this.sigilloFiscaleANN = value;
    }

    /**
     * Recupera il valore della proprietà codSupporto.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCodSupporto() {
        return codSupporto;
    }

    /**
     * Imposta il valore della proprietà codSupporto.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCodSupporto(String value) {
        this.codSupporto = value;
    }

    /**
     * Recupera il valore della proprietà idSupporto.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIdSupporto() {
        return idSupporto;
    }

    /**
     * Imposta il valore della proprietà idSupporto.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIdSupporto(String value) {
        this.idSupporto = value;
    }

    /**
     * Recupera il valore della proprietà idSupAlt.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIdSupAlt() {
        return idSupAlt;
    }

    /**
     * Imposta il valore della proprietà idSupAlt.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIdSupAlt(String value) {
        this.idSupAlt = value;
    }

    /**
     * Recupera il valore della proprietà stato.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getStato() {
        return stato;
    }

    /**
     * Imposta il valore della proprietà stato.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setStato(String value) {
        this.stato = value;
    }

    /**
     * Recupera il valore della proprietà dataIngresso.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDataIngresso() {
        return dataIngresso;
    }

    /**
     * Imposta il valore della proprietà dataIngresso.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDataIngresso(String value) {
        this.dataIngresso = value;
    }

    /**
     * Recupera il valore della proprietà oraIngresso.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getOraIngresso() {
        return oraIngresso;
    }

    /**
     * Imposta il valore della proprietà oraIngresso.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setOraIngresso(String value) {
        this.oraIngresso = value;
    }

	

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if(obj instanceof cnr.isti.sse.big.data.transazioni.Transazione) {
			cnr.isti.sse.big.data.transazioni.Transazione tt = (cnr.isti.sse.big.data.transazioni.Transazione) obj;
			if (!cartaAttivazione.equals(tt.getCartaAttivazione())) {
				return false;
			}
			if (!sigilloFiscale.equals(tt.getSigilloFiscale())) {
				return false;
			}
			if (!progressivoFiscale.equals(tt.getNumeroProgressivo())) {
				return false;
			}
			return true;
		}
		if (getClass() != obj.getClass())
			return false;
		TitoloAccesso other = (TitoloAccesso) obj;
		if (abbonamento == null) {
			if (other.abbonamento != null)
				return false;
		} else if (!abbonamento.equals(other.abbonamento))
			return false;
		if (annullamento == null) {
			if (other.annullamento != null)
				return false;
		} else if (!annullamento.equals(other.annullamento))
			return false;
		if (cartaAttivazione == null) {
			if (other.cartaAttivazione != null)
				return false;
		} else if (!cartaAttivazione.equals(other.cartaAttivazione))
			return false;
		if (cartaAttivazioneANN == null) {
			if (other.cartaAttivazioneANN != null)
				return false;
		} else if (!cartaAttivazioneANN.equals(other.cartaAttivazioneANN))
			return false;
		if (cfAbbonamento == null) {
			if (other.cfAbbonamento != null)
				return false;
		} else if (!cfAbbonamento.equals(other.cfAbbonamento))
			return false;
		if (codSupporto == null) {
			if (other.codSupporto != null)
				return false;
		} else if (!codSupporto.equals(other.codSupporto))
			return false;
		if (codiceAbbonamento == null) {
			if (other.codiceAbbonamento != null)
				return false;
		} else if (!codiceAbbonamento.equals(other.codiceAbbonamento))
			return false;
		if (codiceOrdine == null) {
			if (other.codiceOrdine != null)
				return false;
		} else if (!codiceOrdine.equals(other.codiceOrdine))
			return false;
		if (corrispettivoLordo == null) {
			if (other.corrispettivoLordo != null)
				return false;
		} else if (!corrispettivoLordo.equals(other.corrispettivoLordo))
			return false;
		if (dataANN == null) {
			if (other.dataANN != null)
				return false;
		} else if (!dataANN.equals(other.dataANN))
			return false;
		if (dataEmissione == null) {
			if (other.dataEmissione != null)
				return false;
		} else if (!dataEmissione.equals(other.dataEmissione))
			return false;
		if (dataIngresso == null) {
			if (other.dataIngresso != null)
				return false;
		} else if (!dataIngresso.equals(other.dataIngresso))
			return false;
		if (dataLTA == null) {
			if (other.dataLTA != null)
				return false;
		} else if (!dataLTA.equals(other.dataLTA))
			return false;
		if (idSupAlt == null) {
			if (other.idSupAlt != null)
				return false;
		} else if (!idSupAlt.equals(other.idSupAlt))
			return false;
		if (idSupporto == null) {
			if (other.idSupporto != null)
				return false;
		} else if (!idSupporto.equals(other.idSupporto))
			return false;
		if (oraANN == null) {
			if (other.oraANN != null)
				return false;
		} else if (!oraANN.equals(other.oraANN))
			return false;
		if (oraEmissione == null) {
			if (other.oraEmissione != null)
				return false;
		} else if (!oraEmissione.equals(other.oraEmissione))
			return false;
		if (oraIngresso == null) {
			if (other.oraIngresso != null)
				return false;
		} else if (!oraIngresso.equals(other.oraIngresso))
			return false;
		if (oraLTA == null) {
			if (other.oraLTA != null)
				return false;
		} else if (!oraLTA.equals(other.oraLTA))
			return false;
		if (partecipante == null) {
			if (other.partecipante != null)
				return false;
		} else if (!partecipante.equals(other.partecipante))
			return false;
		if (posto == null) {
			if (other.posto != null)
				return false;
		} else if (!posto.equals(other.posto))
			return false;
		if (progressivoAbbonamento == null) {
			if (other.progressivoAbbonamento != null)
				return false;
		} else if (!progressivoAbbonamento.equals(other.progressivoAbbonamento))
			return false;
		if (progressivoFiscale == null) {
			if (other.progressivoFiscale != null)
				return false;
		} else if (!progressivoFiscale.equals(other.progressivoFiscale))
			return false;
		if (progressivoFiscaleANN == null) {
			if (other.progressivoFiscaleANN != null)
				return false;
		} else if (!progressivoFiscaleANN.equals(other.progressivoFiscaleANN))
			return false;
		if (qEventiAbilitati == null) {
			if (other.qEventiAbilitati != null)
				return false;
		} else if (!qEventiAbilitati.equals(other.qEventiAbilitati))
			return false;
		if (sigilloFiscale == null) {
			if (other.sigilloFiscale != null)
				return false;
		} else if (!sigilloFiscale.equals(other.sigilloFiscale))
			return false;
		if (sigilloFiscaleANN == null) {
			if (other.sigilloFiscaleANN != null)
				return false;
		} else if (!sigilloFiscaleANN.equals(other.sigilloFiscaleANN))
			return false;
		if (sistemaEmissione == null) {
			if (other.sistemaEmissione != null)
				return false;
		} else if (!sistemaEmissione.equals(other.sistemaEmissione))
			return false;
		if (stato == null) {
			if (other.stato != null)
				return false;
		} else if (!stato.equals(other.stato))
			return false;
		if (tipoTitolo == null) {
			if (other.tipoTitolo != null)
				return false;
		} else if (!tipoTitolo.equals(other.tipoTitolo))
			return false;
		return true;
	}
    
    

}
