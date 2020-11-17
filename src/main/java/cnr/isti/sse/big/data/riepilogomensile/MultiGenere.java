//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.11.17 alle 02:47:25 PM CET 
//


package cnr.isti.sse.big.data.riepilogomensile;

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
 *         &lt;element ref="{http://siae.it/mensile}TipoGenere"/>
 *         &lt;element ref="{http://siae.it/mensile}IncidenzaGenere"/>
 *         &lt;element ref="{http://siae.it/mensile}TitoliOpere" maxOccurs="unbounded"/>
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
    "tipoGenere",
    "incidenzaGenere",
    "titoliOpere"
})
@XmlRootElement(name = "MultiGenere")
public class MultiGenere {

    @XmlElement(name = "TipoGenere", required = true)
    protected String tipoGenere;
    @XmlElement(name = "IncidenzaGenere", required = true)
    protected String incidenzaGenere;
    @XmlElement(name = "TitoliOpere", required = true)
    protected List<TitoliOpere> titoliOpere;

    /**
     * Recupera il valore della proprietà tipoGenere.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTipoGenere() {
        return tipoGenere;
    }

    /**
     * Imposta il valore della proprietà tipoGenere.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTipoGenere(String value) {
        this.tipoGenere = value;
    }

    /**
     * Recupera il valore della proprietà incidenzaGenere.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIncidenzaGenere() {
        return incidenzaGenere;
    }

    /**
     * Imposta il valore della proprietà incidenzaGenere.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIncidenzaGenere(String value) {
        this.incidenzaGenere = value;
    }

    /**
     * Gets the value of the titoliOpere property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the titoliOpere property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getTitoliOpere().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link TitoliOpere }
     * 
     * 
     */
    public List<TitoliOpere> getTitoliOpere() {
        if (titoliOpere == null) {
            titoliOpere = new ArrayList<TitoliOpere>();
        }
        return this.titoliOpere;
    }

}
