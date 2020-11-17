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
 *         &lt;element ref="{http://siae.it/mensile}TipoTitolo"/>
 *         &lt;element ref="{http://siae.it/mensile}Quantita"/>
 *         &lt;element ref="{http://siae.it/mensile}CorrispettivoLordo"/>
 *         &lt;element ref="{http://siae.it/mensile}Prevendita"/>
 *         &lt;element ref="{http://siae.it/mensile}IVACorrispettivo"/>
 *         &lt;element ref="{http://siae.it/mensile}IVAPrevendita"/>
 *         &lt;element ref="{http://siae.it/mensile}ImportoPrestazione"/>
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
    "tipoTitolo",
    "quantita",
    "corrispettivoLordo",
    "prevendita",
    "ivaCorrispettivo",
    "ivaPrevendita",
    "importoPrestazione"
})
@XmlRootElement(name = "TitoliAnnullati")
public class TitoliAnnullati {

    @XmlElement(name = "TipoTitolo", required = true)
    protected String tipoTitolo;
    @XmlElement(name = "Quantita", required = true)
    protected String quantita;
    @XmlElement(name = "CorrispettivoLordo", required = true)
    protected String corrispettivoLordo;
    @XmlElement(name = "Prevendita", required = true)
    protected String prevendita;
    @XmlElement(name = "IVACorrispettivo", required = true)
    protected String ivaCorrispettivo;
    @XmlElement(name = "IVAPrevendita", required = true)
    protected String ivaPrevendita;
    @XmlElement(name = "ImportoPrestazione", required = true)
    protected String importoPrestazione;

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
     * Recupera il valore della proprietà quantita.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getQuantita() {
        return quantita;
    }

    /**
     * Imposta il valore della proprietà quantita.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setQuantita(String value) {
        this.quantita = value;
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
     * Recupera il valore della proprietà prevendita.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getPrevendita() {
        return prevendita;
    }

    /**
     * Imposta il valore della proprietà prevendita.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setPrevendita(String value) {
        this.prevendita = value;
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
     * Recupera il valore della proprietà ivaPrevendita.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIVAPrevendita() {
        return ivaPrevendita;
    }

    /**
     * Imposta il valore della proprietà ivaPrevendita.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIVAPrevendita(String value) {
        this.ivaPrevendita = value;
    }

    /**
     * Recupera il valore della proprietà importoPrestazione.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getImportoPrestazione() {
        return importoPrestazione;
    }

    /**
     * Imposta il valore della proprietà importoPrestazione.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setImportoPrestazione(String value) {
        this.importoPrestazione = value;
    }

}
