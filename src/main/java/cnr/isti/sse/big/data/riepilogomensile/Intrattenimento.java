//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.11.17 alle 02:47:25 PM CET 
//


package cnr.isti.sse.big.data.riepilogomensile;

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
 *         &lt;element ref="{http://siae.it/mensile}TipoTassazione"/>
 *         &lt;element ref="{http://siae.it/mensile}Incidenza" minOccurs="0"/>
 *         &lt;element ref="{http://siae.it/mensile}ImponibileIntrattenimenti" minOccurs="0"/>
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
    "tipoTassazione",
    "incidenza",
    "imponibileIntrattenimenti"
})
@XmlRootElement(name = "Intrattenimento")
public class Intrattenimento {

    @XmlElement(name = "TipoTassazione", required = true)
    protected TipoTassazione tipoTassazione;
    @XmlElement(name = "Incidenza")
    protected String incidenza;
    @XmlElement(name = "ImponibileIntrattenimenti")
    protected String imponibileIntrattenimenti;

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
     * Recupera il valore della proprietà incidenza.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIncidenza() {
        return incidenza;
    }

    /**
     * Imposta il valore della proprietà incidenza.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIncidenza(String value) {
        this.incidenza = value;
    }

    /**
     * Recupera il valore della proprietà imponibileIntrattenimenti.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getImponibileIntrattenimenti() {
        return imponibileIntrattenimenti;
    }

    /**
     * Imposta il valore della proprietà imponibileIntrattenimenti.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setImponibileIntrattenimenti(String value) {
        this.imponibileIntrattenimenti = value;
    }

}
