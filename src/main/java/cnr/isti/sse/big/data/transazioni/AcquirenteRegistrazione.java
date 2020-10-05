//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.10.05 alle 12:50:22 PM CEST 
//


package cnr.isti.sse.big.data.transazioni;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.adapters.CollapsedStringAdapter;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;


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
 *         &lt;element ref="{}CodiceUnivocoAcquirente"/>
 *         &lt;element ref="{}IndirizzoIPRegistrazione"/>
 *         &lt;element ref="{}DataOraRegistrazione"/>
 *       &lt;/sequence>
 *       &lt;attribute name="Autenticazione" use="required">
 *         &lt;simpleType>
 *           &lt;restriction base="{http://www.w3.org/2001/XMLSchema}NMTOKEN">
 *             &lt;enumeration value="SPID"/>
 *             &lt;enumeration value="OTP"/>
 *             &lt;enumeration value="BO"/>
 *           &lt;/restriction>
 *         &lt;/simpleType>
 *       &lt;/attribute>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "codiceUnivocoAcquirente",
    "indirizzoIPRegistrazione",
    "dataOraRegistrazione"
})
@XmlRootElement(name = "AcquirenteRegistrazione")
public class AcquirenteRegistrazione {

    @XmlElement(name = "CodiceUnivocoAcquirente", required = true)
    protected String codiceUnivocoAcquirente;
    @XmlElement(name = "IndirizzoIPRegistrazione", required = true)
    protected String indirizzoIPRegistrazione;
    @XmlElement(name = "DataOraRegistrazione", required = true)
    protected String dataOraRegistrazione;
    @XmlAttribute(name = "Autenticazione", required = true)
    @XmlJavaTypeAdapter(CollapsedStringAdapter.class)
    protected String autenticazione;

    /**
     * Recupera il valore della proprietà codiceUnivocoAcquirente.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCodiceUnivocoAcquirente() {
        return codiceUnivocoAcquirente;
    }

    /**
     * Imposta il valore della proprietà codiceUnivocoAcquirente.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCodiceUnivocoAcquirente(String value) {
        this.codiceUnivocoAcquirente = value;
    }

    /**
     * Recupera il valore della proprietà indirizzoIPRegistrazione.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIndirizzoIPRegistrazione() {
        return indirizzoIPRegistrazione;
    }

    /**
     * Imposta il valore della proprietà indirizzoIPRegistrazione.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIndirizzoIPRegistrazione(String value) {
        this.indirizzoIPRegistrazione = value;
    }

    /**
     * Recupera il valore della proprietà dataOraRegistrazione.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDataOraRegistrazione() {
        return dataOraRegistrazione;
    }

    /**
     * Imposta il valore della proprietà dataOraRegistrazione.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDataOraRegistrazione(String value) {
        this.dataOraRegistrazione = value;
    }

    /**
     * Recupera il valore della proprietà autenticazione.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getAutenticazione() {
        return autenticazione;
    }

    /**
     * Imposta il valore della proprietà autenticazione.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setAutenticazione(String value) {
        this.autenticazione = value;
    }

}
