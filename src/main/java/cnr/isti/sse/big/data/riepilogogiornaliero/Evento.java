//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.11.17 alle 02:46:45 PM CET 
//


package cnr.isti.sse.big.data.riepilogogiornaliero;

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
 *         &lt;element ref="{http://siae.it/gionaliero}Intrattenimento"/>
 *         &lt;element ref="{http://siae.it/gionaliero}Locale"/>
 *         &lt;element ref="{http://siae.it/gionaliero}Data"/>
 *         &lt;element ref="{http://siae.it/gionaliero}Ora"/>
 *         &lt;element ref="{http://siae.it/gionaliero}MultiGenere" maxOccurs="unbounded"/>
 *         &lt;element ref="{http://siae.it/gionaliero}OrdineDiPosto" maxOccurs="unbounded"/>
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
    "intrattenimento",
    "locale",
    "data",
    "ora",
    "multiGenere",
    "ordineDiPosto"
})
@XmlRootElement(name = "Evento")
public class Evento {

    @XmlElement(name = "Intrattenimento", required = true)
    protected Intrattenimento intrattenimento;
    @XmlElement(name = "Locale", required = true)
    protected Locale locale;
    @XmlElement(name = "Data", required = true)
    protected String data;
    @XmlElement(name = "Ora", required = true)
    protected String ora;
    @XmlElement(name = "MultiGenere", required = true)
    protected List<MultiGenere> multiGenere;
    @XmlElement(name = "OrdineDiPosto", required = true)
    protected List<OrdineDiPosto> ordineDiPosto;

    /**
     * Recupera il valore della proprietà intrattenimento.
     * 
     * @return
     *     possible object is
     *     {@link Intrattenimento }
     *     
     */
    public Intrattenimento getIntrattenimento() {
        return intrattenimento;
    }

    /**
     * Imposta il valore della proprietà intrattenimento.
     * 
     * @param value
     *     allowed object is
     *     {@link Intrattenimento }
     *     
     */
    public void setIntrattenimento(Intrattenimento value) {
        this.intrattenimento = value;
    }

    /**
     * Recupera il valore della proprietà locale.
     * 
     * @return
     *     possible object is
     *     {@link Locale }
     *     
     */
    public Locale getLocale() {
        return locale;
    }

    /**
     * Imposta il valore della proprietà locale.
     * 
     * @param value
     *     allowed object is
     *     {@link Locale }
     *     
     */
    public void setLocale(Locale value) {
        this.locale = value;
    }

    /**
     * Recupera il valore della proprietà data.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getData() {
        return data;
    }

    /**
     * Imposta il valore della proprietà data.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setData(String value) {
        this.data = value;
    }

    /**
     * Recupera il valore della proprietà ora.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getOra() {
        return ora;
    }

    /**
     * Imposta il valore della proprietà ora.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setOra(String value) {
        this.ora = value;
    }

    /**
     * Gets the value of the multiGenere property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the multiGenere property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getMultiGenere().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link MultiGenere }
     * 
     * 
     */
    public List<MultiGenere> getMultiGenere() {
        if (multiGenere == null) {
            multiGenere = new ArrayList<MultiGenere>();
        }
        return this.multiGenere;
    }

    /**
     * Gets the value of the ordineDiPosto property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the ordineDiPosto property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getOrdineDiPosto().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link OrdineDiPosto }
     * 
     * 
     */
    public List<OrdineDiPosto> getOrdineDiPosto() {
        if (ordineDiPosto == null) {
            ordineDiPosto = new ArrayList<OrdineDiPosto>();
        }
        return this.ordineDiPosto;
    }

}
