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
 *         &lt;element ref="{http://siae.it/mensile}Titolare"/>
 *         &lt;element ref="{http://siae.it/mensile}Organizzatore" maxOccurs="unbounded" minOccurs="0"/>
 *       &lt;/sequence>
 *       &lt;attribute name="Sostituzione" use="required">
 *         &lt;simpleType>
 *           &lt;restriction base="{http://www.w3.org/2001/XMLSchema}NMTOKEN">
 *             &lt;enumeration value="N"/>
 *             &lt;enumeration value="S"/>
 *           &lt;/restriction>
 *         &lt;/simpleType>
 *       &lt;/attribute>
 *       &lt;attribute name="Mese" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="Valuta" default="E">
 *         &lt;simpleType>
 *           &lt;restriction base="{http://www.w3.org/2001/XMLSchema}NMTOKEN">
 *             &lt;enumeration value="E"/>
 *             &lt;enumeration value="L"/>
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
    "titolare",
    "organizzatore"
})
@XmlRootElement(name = "RiepilogoMensile")
public class RiepilogoMensile {

    @XmlElement(name = "Titolare", required = true)
    protected Titolare titolare;
    @XmlElement(name = "Organizzatore")
    protected List<Organizzatore> organizzatore;
    @XmlAttribute(name = "Sostituzione", required = true)
    @XmlJavaTypeAdapter(CollapsedStringAdapter.class)
    protected String sostituzione;
    @XmlAttribute(name = "Mese", required = true)
    protected String mese;
    @XmlAttribute(name = "DataGenerazione", required = true)
    protected String datagenerazione;
    @XmlAttribute(name = "OraGenerazione", required = true)
    protected String oragenerazione;
    @XmlAttribute(name = "ProgressivoGenerazione", required = true)
    protected String progressivogenerazione;
    @XmlAttribute(name = "Valuta")
    @XmlJavaTypeAdapter(CollapsedStringAdapter.class)
    protected String valuta;

    /**
     * Recupera il valore della proprietà titolare.
     * 
     * @return
     *     possible object is
     *     {@link Titolare }
     *     
     */
    public Titolare getTitolare() {
        return titolare;
    }

    /**
     * Imposta il valore della proprietà titolare.
     * 
     * @param value
     *     allowed object is
     *     {@link Titolare }
     *     
     */
    public void setTitolare(Titolare value) {
        this.titolare = value;
    }

    /**
     * Gets the value of the organizzatore property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the organizzatore property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getOrganizzatore().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link Organizzatore }
     * 
     * 
     */
    public List<Organizzatore> getOrganizzatore() {
        if (organizzatore == null) {
            organizzatore = new ArrayList<Organizzatore>();
        }
        return this.organizzatore;
    }

    /**
     * Recupera il valore della proprietà sostituzione.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getSostituzione() {
        return sostituzione;
    }

    /**
     * Imposta il valore della proprietà sostituzione.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSostituzione(String value) {
        this.sostituzione = value;
    }

    /**
     * Recupera il valore della proprietà mese.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getMese() {
        return mese;
    }

    /**
     * Imposta il valore della proprietà mese.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setMese(String value) {
        this.mese = value;
    }

    /**
     * Recupera il valore della proprietà valuta.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getValuta() {
        if (valuta == null) {
            return "E";
        } else {
            return valuta;
        }
    }

    /**
     * Imposta il valore della proprietà valuta.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setValuta(String value) {
        this.valuta = value;
    }

	public String getDatagenerazione() {
		return datagenerazione;
	}

	public void setDatagenerazione(String datagenerazione) {
		this.datagenerazione = datagenerazione;
	}

	public String getOragenerazione() {
		return oragenerazione;
	}

	public void setOragenerazione(String oragenerazione) {
		this.oragenerazione = oragenerazione;
	}

	public String getProgressivogenerazione() {
		return progressivogenerazione;
	}

	public void setProgressivogenerazione(String progressivogenerazione) {
		this.progressivogenerazione = progressivogenerazione;
	}

	public void setOrganizzatore(List<Organizzatore> organizzatore) {
		this.organizzatore = organizzatore;
	}

    
}
