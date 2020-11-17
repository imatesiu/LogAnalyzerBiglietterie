//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.11.17 alle 02:46:45 PM CET 
//


package cnr.isti.sse.big.data.riepilogogiornaliero;

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
 *         &lt;element ref="{http://siae.it/gionaliero}TipoTassazione"/>
 *         &lt;element ref="{http://siae.it/gionaliero}Incidenza" minOccurs="0"/>
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
    "incidenza"
})
@XmlRootElement(name = "Intrattenimento")
public class Intrattenimento {

    @XmlElement(name = "TipoTassazione", required = true)
    protected TipoTassazione tipoTassazione;
    @XmlElement(name = "Incidenza")
    protected String incidenza;

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

}
