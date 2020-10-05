//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.10.05 alle 12:50:22 PM CEST 
//


package cnr.isti.sse.big.data.transazioni;

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
 *         &lt;element ref="{}CodicePrestazione"/>
 *         &lt;element ref="{}ImportoPrestazione"/>
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
    "codicePrestazione",
    "importoPrestazione"
})
@XmlRootElement(name = "Complementare")
public class Complementare {

    @XmlElement(name = "CodicePrestazione", required = true)
    protected String codicePrestazione;
    @XmlElement(name = "ImportoPrestazione", required = true)
    protected String importoPrestazione;

    /**
     * Recupera il valore della proprietà codicePrestazione.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCodicePrestazione() {
        return codicePrestazione;
    }

    /**
     * Imposta il valore della proprietà codicePrestazione.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCodicePrestazione(String value) {
        this.codicePrestazione = value;
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
