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
 *         &lt;element ref="{http://siae.it/mensile}Quantita"/>
 *         &lt;element ref="{http://siae.it/mensile}ImportoFiqurativo"/>
 *         &lt;element ref="{http://siae.it/mensile}IVAFiqurativa"/>
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
    "importoFiqurativo",
    "ivaFiqurativa"
})
@XmlRootElement(name = "AbbonamentiIVAPreassoltaAnnullati")
public class AbbonamentiIVAPreassoltaAnnullati {

    @XmlElement(name = "Quantita", required = true)
    protected String quantita;
    @XmlElement(name = "ImportoFiqurativo", required = true)
    protected String importoFiqurativo;
    @XmlElement(name = "IVAFiqurativa", required = true)
    protected String ivaFiqurativa;

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
     * Recupera il valore della proprietà importoFiqurativo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getImportoFiqurativo() {
        return importoFiqurativo;
    }

    /**
     * Imposta il valore della proprietà importoFiqurativo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setImportoFiqurativo(String value) {
        this.importoFiqurativo = value;
    }

    /**
     * Recupera il valore della proprietà ivaFiqurativa.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIVAFiqurativa() {
        return ivaFiqurativa;
    }

    /**
     * Imposta il valore della proprietà ivaFiqurativa.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIVAFiqurativa(String value) {
        this.ivaFiqurativa = value;
    }

}
