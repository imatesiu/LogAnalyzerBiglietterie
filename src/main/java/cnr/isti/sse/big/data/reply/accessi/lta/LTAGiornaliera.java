//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.11.18 alle 10:56:34 PM CET 
//


package cnr.isti.sse.big.data.reply.accessi.lta;

import java.util.ArrayList;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
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
 *         &lt;element ref="{http://tempuri.org/lta}LTA_Evento" maxOccurs="unbounded"/>
 *       &lt;/sequence>
 *       &lt;attribute name="SistemaCA" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CFTitolareCA" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="DataLTA" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "ltaEvento"
})
@XmlRootElement(name = "LTA_Giornaliera")
public class LTAGiornaliera {

    @XmlElement(name = "LTA_Evento", required = true)
    protected List<LTAEvento> ltaEvento;
    @XmlAttribute(name = "SistemaCA", required = true)
    protected String sistemaCA;
    @XmlAttribute(name = "CFTitolareCA", required = true)
    protected String cfTitolareCA;
    @XmlAttribute(name = "DataLTA", required = true)
    protected String dataLTA;

    /**
     * Gets the value of the ltaEvento property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the ltaEvento property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getLTAEvento().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link LTAEvento }
     * 
     * 
     */
    public List<LTAEvento> getLTAEvento() {
        if (ltaEvento == null) {
            ltaEvento = new ArrayList<LTAEvento>();
        }
        return this.ltaEvento;
    }

    /**
     * Recupera il valore della proprietà sistemaCA.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getSistemaCA() {
        return sistemaCA;
    }

    /**
     * Imposta il valore della proprietà sistemaCA.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSistemaCA(String value) {
        this.sistemaCA = value;
    }

    /**
     * Recupera il valore della proprietà cfTitolareCA.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCFTitolareCA() {
        return cfTitolareCA;
    }

    /**
     * Imposta il valore della proprietà cfTitolareCA.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCFTitolareCA(String value) {
        this.cfTitolareCA = value;
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

}
