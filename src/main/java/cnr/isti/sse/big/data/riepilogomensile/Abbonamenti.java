//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.11.17 alle 02:47:25 PM CET 
//


package cnr.isti.sse.big.data.riepilogomensile;

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
 *         &lt;element ref="{http://siae.it/mensile}CodiceAbbonamento"/>
 *         &lt;element ref="{http://siae.it/mensile}Validita"/>
 *         &lt;element ref="{http://siae.it/mensile}TipoTassazione"/>
 *         &lt;element ref="{http://siae.it/mensile}Turno"/>
 *         &lt;element ref="{http://siae.it/mensile}CodiceOrdine"/>
 *         &lt;element ref="{http://siae.it/mensile}TipoTitolo"/>
 *         &lt;element ref="{http://siae.it/mensile}QuantitaEventiAbilitati"/>
 *         &lt;element ref="{http://siae.it/mensile}AbbonamentiEmessi" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element ref="{http://siae.it/mensile}AbbonamentiAnnullati" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element ref="{http://siae.it/mensile}AbbonamentiIVAPreassolta" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element ref="{http://siae.it/mensile}AbbonamentiIVAPreassoltaAnnullati" maxOccurs="unbounded" minOccurs="0"/>
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
    "codiceAbbonamento",
    "validita",
    "tipoTassazione",
    "turno",
    "codiceOrdine",
    "tipoTitolo",
    "quantitaEventiAbilitati",
    "abbonamentiEmessi",
    "abbonamentiAnnullati",
    "abbonamentiIVAPreassolta",
    "abbonamentiIVAPreassoltaAnnullati"
})
@XmlRootElement(name = "Abbonamenti")
public class Abbonamenti {

    @XmlElement(name = "CodiceAbbonamento", required = true)
    protected String codiceAbbonamento;
    @XmlElement(name = "Validita", required = true)
    protected String validita;
    @XmlElement(name = "TipoTassazione", required = true)
    protected TipoTassazione tipoTassazione;
    @XmlElement(name = "Turno", required = true)
    protected Turno turno;
    @XmlElement(name = "CodiceOrdine", required = true)
    protected String codiceOrdine;
    @XmlElement(name = "TipoTitolo", required = true)
    protected String tipoTitolo;
    @XmlElement(name = "QuantitaEventiAbilitati", required = true)
    protected String quantitaEventiAbilitati;
    @XmlElement(name = "AbbonamentiEmessi")
    protected List<AbbonamentiEmessi> abbonamentiEmessi;
    @XmlElement(name = "AbbonamentiAnnullati")
    protected List<AbbonamentiAnnullati> abbonamentiAnnullati;
    @XmlElement(name = "AbbonamentiIVAPreassolta")
    protected List<AbbonamentiIVAPreassolta> abbonamentiIVAPreassolta;
    @XmlElement(name = "AbbonamentiIVAPreassoltaAnnullati")
    protected List<AbbonamentiIVAPreassoltaAnnullati> abbonamentiIVAPreassoltaAnnullati;

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
     * Recupera il valore della proprietà validita.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getValidita() {
        return validita;
    }

    /**
     * Imposta il valore della proprietà validita.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setValidita(String value) {
        this.validita = value;
    }

    /**
     * Recupera il valore della proprietà tipoTassazione.
     * 
     * @return
     *     possible object is
     *     {@link TipoTassazione }
     *     
     */
    public TipoTassazione getTipoTassazione() {
        return tipoTassazione;
    }

    /**
     * Imposta il valore della proprietà tipoTassazione.
     * 
     * @param value
     *     allowed object is
     *     {@link TipoTassazione }
     *     
     */
    public void setTipoTassazione(TipoTassazione value) {
        this.tipoTassazione = value;
    }

    /**
     * Recupera il valore della proprietà turno.
     * 
     * @return
     *     possible object is
     *     {@link Turno }
     *     
     */
    public Turno getTurno() {
        return turno;
    }

    /**
     * Imposta il valore della proprietà turno.
     * 
     * @param value
     *     allowed object is
     *     {@link Turno }
     *     
     */
    public void setTurno(Turno value) {
        this.turno = value;
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
     * Recupera il valore della proprietà quantitaEventiAbilitati.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getQuantitaEventiAbilitati() {
        return quantitaEventiAbilitati;
    }

    /**
     * Imposta il valore della proprietà quantitaEventiAbilitati.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setQuantitaEventiAbilitati(String value) {
        this.quantitaEventiAbilitati = value;
    }

    /**
     * Gets the value of the abbonamentiEmessi property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the abbonamentiEmessi property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getAbbonamentiEmessi().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link AbbonamentiEmessi }
     * 
     * 
     */
    public List<AbbonamentiEmessi> getAbbonamentiEmessi() {
        if (abbonamentiEmessi == null) {
            abbonamentiEmessi = new ArrayList<AbbonamentiEmessi>();
        }
        return this.abbonamentiEmessi;
    }

    /**
     * Gets the value of the abbonamentiAnnullati property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the abbonamentiAnnullati property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getAbbonamentiAnnullati().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link AbbonamentiAnnullati }
     * 
     * 
     */
    public List<AbbonamentiAnnullati> getAbbonamentiAnnullati() {
        if (abbonamentiAnnullati == null) {
            abbonamentiAnnullati = new ArrayList<AbbonamentiAnnullati>();
        }
        return this.abbonamentiAnnullati;
    }

    /**
     * Gets the value of the abbonamentiIVAPreassolta property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the abbonamentiIVAPreassolta property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getAbbonamentiIVAPreassolta().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link AbbonamentiIVAPreassolta }
     * 
     * 
     */
    public List<AbbonamentiIVAPreassolta> getAbbonamentiIVAPreassolta() {
        if (abbonamentiIVAPreassolta == null) {
            abbonamentiIVAPreassolta = new ArrayList<AbbonamentiIVAPreassolta>();
        }
        return this.abbonamentiIVAPreassolta;
    }

    /**
     * Gets the value of the abbonamentiIVAPreassoltaAnnullati property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the abbonamentiIVAPreassoltaAnnullati property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getAbbonamentiIVAPreassoltaAnnullati().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link AbbonamentiIVAPreassoltaAnnullati }
     * 
     * 
     */
    public List<AbbonamentiIVAPreassoltaAnnullati> getAbbonamentiIVAPreassoltaAnnullati() {
        if (abbonamentiIVAPreassoltaAnnullati == null) {
            abbonamentiIVAPreassoltaAnnullati = new ArrayList<AbbonamentiIVAPreassoltaAnnullati>();
        }
        return this.abbonamentiIVAPreassoltaAnnullati;
    }

}
