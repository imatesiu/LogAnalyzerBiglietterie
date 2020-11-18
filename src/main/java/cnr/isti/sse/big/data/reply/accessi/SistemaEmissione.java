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
 *         &lt;element ref="{http://tempuri.org/accessi}Titoli" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element ref="{http://tempuri.org/accessi}Abbonamenti" maxOccurs="unbounded" minOccurs="0"/>
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
    "titoli",
    "abbonamenti"
})
@XmlRootElement(name = "SistemaEmissione")
public class SistemaEmissione {

    @XmlElement(name = "Titoli")
    protected List<Titoli> titoli;
    @XmlElement(name = "Abbonamenti")
    protected List<Abbonamenti> abbonamenti;

    /**
     * Gets the value of the titoli property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the titoli property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getTitoli().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link Titoli }
     * 
     * 
     */
    public List<Titoli> getTitoli() {
        if (titoli == null) {
            titoli = new ArrayList<Titoli>();
        }
        return this.titoli;
    }

    /**
     * Gets the value of the abbonamenti property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the abbonamenti property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getAbbonamenti().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link Abbonamenti }
     * 
     * 
     */
    public List<Abbonamenti> getAbbonamenti() {
        if (abbonamenti == null) {
            abbonamenti = new ArrayList<Abbonamenti>();
        }
        return this.abbonamenti;
    }

}
