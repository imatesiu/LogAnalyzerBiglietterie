//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.11.18 alle 08:39:48 PM CET 
//


package cnr.isti.sse.big.data.reply.accessi;

import java.util.ArrayList;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;


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
 *         &lt;element ref="{http://tempuri.org/accessi}CFOrganizzatore"/>
 *         &lt;element ref="{http://tempuri.org/accessi}DenominazioneOrganizzatore"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TipologiaOrganizzatore"/>
 *         &lt;element ref="{http://tempuri.org/accessi}SpettacoloIntrattenimento"/>
 *         &lt;element ref="{http://tempuri.org/accessi}IncidenzaIntrattenimento"/>
 *         &lt;element ref="{http://tempuri.org/accessi}DenominazioneLocale"/>
 *         &lt;element ref="{http://tempuri.org/accessi}CodiceLocale"/>
 *         &lt;element ref="{http://tempuri.org/accessi}DataEvento"/>
 *         &lt;element ref="{http://tempuri.org/accessi}OraEvento"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TipoGenere"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TitoloEvento"/>
 *         &lt;element ref="{http://tempuri.org/accessi}Autore"/>
 *         &lt;element ref="{http://tempuri.org/accessi}Esecutore"/>
 *         &lt;element ref="{http://tempuri.org/accessi}NazionalitaFilm"/>
 *         &lt;element ref="{http://tempuri.org/accessi}NumOpereRappresentate"/>
 *         &lt;element ref="{http://tempuri.org/accessi}SistemaEmissione" maxOccurs="unbounded"/>
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
    "cfOrganizzatore",
    "denominazioneOrganizzatore",
    "tipologiaOrganizzatore",
    "spettacoloIntrattenimento",
    "incidenzaIntrattenimento",
    "denominazioneLocale",
    "codiceLocale",
    "dataEvento",
    "oraEvento",
    "tipoGenere",
    "titoloEvento",
    "autore",
    "esecutore",
    "nazionalitaFilm",
    "numOpereRappresentate",
    "sistemaEmissione"
})
@XmlRootElement(name = "Evento")
public class Evento {

    @XmlElement(name = "CFOrganizzatore", required = true)
    protected String cfOrganizzatore;
    @XmlElement(name = "DenominazioneOrganizzatore", required = true)
    protected String denominazioneOrganizzatore;
    @XmlElement(name = "TipologiaOrganizzatore", required = true)
    protected String tipologiaOrganizzatore;
    @XmlElement(name = "SpettacoloIntrattenimento", required = true)
    protected String spettacoloIntrattenimento;
    @XmlElement(name = "IncidenzaIntrattenimento", required = true)
    protected String incidenzaIntrattenimento;
    @XmlElement(name = "DenominazioneLocale", required = true)
    protected String denominazioneLocale;
    @XmlElement(name = "CodiceLocale", required = true)
    protected String codiceLocale;
    @XmlElement(name = "DataEvento", required = true)
    protected String dataEvento;
    @XmlElement(name = "OraEvento", required = true)
    protected String oraEvento;
    @XmlElement(name = "TipoGenere", required = true)
    protected String tipoGenere;
    @XmlElement(name = "TitoloEvento", required = true)
    protected String titoloEvento;
    @XmlElement(name = "Autore", required = true)
    protected String autore;
    @XmlElement(name = "Esecutore", required = true)
    protected String esecutore;
    @XmlElement(name = "NazionalitaFilm", required = true)
    protected String nazionalitaFilm;
    @XmlElement(name = "NumOpereRappresentate", required = true)
    protected String numOpereRappresentate;
    @XmlElement(name = "SistemaEmissione", required = true)
    protected List<SistemaEmissione> sistemaEmissione;

    /**
     * Recupera il valore della proprietà cfOrganizzatore.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCFOrganizzatore() {
        return cfOrganizzatore;
    }

    /**
     * Imposta il valore della proprietà cfOrganizzatore.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCFOrganizzatore(String value) {
        this.cfOrganizzatore = value;
    }

    /**
     * Recupera il valore della proprietà denominazioneOrganizzatore.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDenominazioneOrganizzatore() {
        return denominazioneOrganizzatore;
    }

    /**
     * Imposta il valore della proprietà denominazioneOrganizzatore.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDenominazioneOrganizzatore(String value) {
        this.denominazioneOrganizzatore = value;
    }

    /**
     * Recupera il valore della proprietà tipologiaOrganizzatore.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTipologiaOrganizzatore() {
        return tipologiaOrganizzatore;
    }

    /**
     * Imposta il valore della proprietà tipologiaOrganizzatore.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTipologiaOrganizzatore(String value) {
        this.tipologiaOrganizzatore = value;
    }

    /**
     * Recupera il valore della proprietà spettacoloIntrattenimento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getSpettacoloIntrattenimento() {
        return spettacoloIntrattenimento;
    }

    /**
     * Imposta il valore della proprietà spettacoloIntrattenimento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSpettacoloIntrattenimento(String value) {
        this.spettacoloIntrattenimento = value;
    }

    /**
     * Recupera il valore della proprietà incidenzaIntrattenimento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIncidenzaIntrattenimento() {
        return incidenzaIntrattenimento;
    }

    /**
     * Imposta il valore della proprietà incidenzaIntrattenimento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIncidenzaIntrattenimento(String value) {
        this.incidenzaIntrattenimento = value;
    }

    /**
     * Recupera il valore della proprietà denominazioneLocale.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDenominazioneLocale() {
        return denominazioneLocale;
    }

    /**
     * Imposta il valore della proprietà denominazioneLocale.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDenominazioneLocale(String value) {
        this.denominazioneLocale = value;
    }

    /**
     * Recupera il valore della proprietà codiceLocale.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCodiceLocale() {
        return codiceLocale;
    }

    /**
     * Imposta il valore della proprietà codiceLocale.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCodiceLocale(String value) {
        this.codiceLocale = value;
    }

    /**
     * Recupera il valore della proprietà dataEvento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDataEvento() {
        return dataEvento;
    }

    /**
     * Imposta il valore della proprietà dataEvento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDataEvento(String value) {
        this.dataEvento = value;
    }

    /**
     * Recupera il valore della proprietà oraEvento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getOraEvento() {
        return oraEvento;
    }

    /**
     * Imposta il valore della proprietà oraEvento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setOraEvento(String value) {
        this.oraEvento = value;
    }

    /**
     * Recupera il valore della proprietà tipoGenere.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTipoGenere() {
        return tipoGenere;
    }

    /**
     * Imposta il valore della proprietà tipoGenere.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTipoGenere(String value) {
        this.tipoGenere = value;
    }

    /**
     * Recupera il valore della proprietà titoloEvento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTitoloEvento() {
        return titoloEvento;
    }

    /**
     * Imposta il valore della proprietà titoloEvento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTitoloEvento(String value) {
        this.titoloEvento = value;
    }

    /**
     * Recupera il valore della proprietà autore.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getAutore() {
        return autore;
    }

    /**
     * Imposta il valore della proprietà autore.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setAutore(String value) {
        this.autore = value;
    }

    /**
     * Recupera il valore della proprietà esecutore.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getEsecutore() {
        return esecutore;
    }

    /**
     * Imposta il valore della proprietà esecutore.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setEsecutore(String value) {
        this.esecutore = value;
    }

    /**
     * Recupera il valore della proprietà nazionalitaFilm.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getNazionalitaFilm() {
        return nazionalitaFilm;
    }

    /**
     * Imposta il valore della proprietà nazionalitaFilm.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setNazionalitaFilm(String value) {
        this.nazionalitaFilm = value;
    }

    /**
     * Recupera il valore della proprietà numOpereRappresentate.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getNumOpereRappresentate() {
        return numOpereRappresentate;
    }

    /**
     * Imposta il valore della proprietà numOpereRappresentate.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setNumOpereRappresentate(String value) {
        this.numOpereRappresentate = value;
    }

    /**
     * Gets the value of the sistemaEmissione property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the sistemaEmissione property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getSistemaEmissione().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link SistemaEmissione }
     * 
     * 
     */
    public List<SistemaEmissione> getSistemaEmissione() {
        if (sistemaEmissione == null) {
            sistemaEmissione = new ArrayList<SistemaEmissione>();
        }
        return this.sistemaEmissione;
    }

}
