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
 *         &lt;element ref="{http://siae.it/mensile}TipoProvento"/>
 *         &lt;element ref="{http://siae.it/mensile}CorrispettivoLordo"/>
 *         &lt;element ref="{http://siae.it/mensile}IVACorrispettivo"/>
 *         &lt;element ref="{http://siae.it/mensile}GenerePrevalente"/>
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
    "tipoProvento",
    "corrispettivoLordo",
    "ivaCorrispettivo",
    "generePrevalente"
})
@XmlRootElement(name = "AltriProventiGenerici")
public class AltriProventiGenerici {

    @XmlElement(name = "TipoProvento", required = true)
    protected String tipoProvento;
    @XmlElement(name = "CorrispettivoLordo", required = true)
    protected String corrispettivoLordo;
    @XmlElement(name = "IVACorrispettivo", required = true)
    protected String ivaCorrispettivo;
    @XmlElement(name = "GenerePrevalente", required = true)
    protected String generePrevalente;

    /**
     * Recupera il valore della proprietà tipoProvento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTipoProvento() {
        return tipoProvento;
    }

    /**
     * Imposta il valore della proprietà tipoProvento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTipoProvento(String value) {
        this.tipoProvento = value;
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
     * Recupera il valore della proprietà ivaCorrispettivo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIVACorrispettivo() {
        return ivaCorrispettivo;
    }

    /**
     * Imposta il valore della proprietà ivaCorrispettivo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIVACorrispettivo(String value) {
        this.ivaCorrispettivo = value;
    }

    /**
     * Recupera il valore della proprietà generePrevalente.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getGenerePrevalente() {
        return generePrevalente;
    }

    /**
     * Imposta il valore della proprietà generePrevalente.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setGenerePrevalente(String value) {
        this.generePrevalente = value;
    }

}
