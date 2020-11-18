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
 *         &lt;element ref="{http://tempuri.org/accessi}CodiceOrdinePosto"/>
 *         &lt;element ref="{http://tempuri.org/accessi}Capienza"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTipoTitoloAbbonamento" maxOccurs="unbounded"/>
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
    "codiceOrdinePosto",
    "capienza",
    "totaleTipoTitoloAbbonamento"
})
@XmlRootElement(name = "Abbonamenti")
public class Abbonamenti {

    @XmlElement(name = "CodiceOrdinePosto", required = true)
    protected String codiceOrdinePosto;
    @XmlElement(name = "Capienza", required = true)
    protected String capienza;
    @XmlElement(name = "TotaleTipoTitoloAbbonamento", required = true)
    protected List<TotaleTipoTitoloAbbonamento> totaleTipoTitoloAbbonamento;

    /**
     * Recupera il valore della proprietà codiceOrdinePosto.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCodiceOrdinePosto() {
        return codiceOrdinePosto;
    }

    /**
     * Imposta il valore della proprietà codiceOrdinePosto.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCodiceOrdinePosto(String value) {
        this.codiceOrdinePosto = value;
    }

    /**
     * Recupera il valore della proprietà capienza.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCapienza() {
        return capienza;
    }

    /**
     * Imposta il valore della proprietà capienza.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCapienza(String value) {
        this.capienza = value;
    }

    /**
     * Gets the value of the totaleTipoTitoloAbbonamento property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the totaleTipoTitoloAbbonamento property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getTotaleTipoTitoloAbbonamento().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link TotaleTipoTitoloAbbonamento }
     * 
     * 
     */
    public List<TotaleTipoTitoloAbbonamento> getTotaleTipoTitoloAbbonamento() {
        if (totaleTipoTitoloAbbonamento == null) {
            totaleTipoTitoloAbbonamento = new ArrayList<TotaleTipoTitoloAbbonamento>();
        }
        return this.totaleTipoTitoloAbbonamento;
    }

}
