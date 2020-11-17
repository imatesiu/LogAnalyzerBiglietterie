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
 *         &lt;element ref="{http://siae.it/gionaliero}CodiceOrdine"/>
 *         &lt;element ref="{http://siae.it/gionaliero}Capienza"/>
 *         &lt;element ref="{http://siae.it/gionaliero}TitoliAccesso" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element ref="{http://siae.it/gionaliero}TitoliAnnullati" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element ref="{http://siae.it/gionaliero}TitoliAccessoIVAPreassolta" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element ref="{http://siae.it/gionaliero}TitoliIVAPreassoltaAnnullati" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element ref="{http://siae.it/gionaliero}BigliettiAbbonamento" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element ref="{http://siae.it/gionaliero}BigliettiAbbonamentoAnnullati" maxOccurs="unbounded" minOccurs="0"/>
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
    "codiceOrdine",
    "capienza",
    "titoliAccesso",
    "titoliAnnullati",
    "titoliAccessoIVAPreassolta",
    "titoliIVAPreassoltaAnnullati",
    "bigliettiAbbonamento",
    "bigliettiAbbonamentoAnnullati"
})
@XmlRootElement(name = "OrdineDiPosto")
public class OrdineDiPosto {

    @XmlElement(name = "CodiceOrdine", required = true)
    protected String codiceOrdine;
    @XmlElement(name = "Capienza", required = true)
    protected String capienza;
    @XmlElement(name = "TitoliAccesso")
    protected List<TitoliAccesso> titoliAccesso;
    @XmlElement(name = "TitoliAnnullati")
    protected List<TitoliAnnullati> titoliAnnullati;
    @XmlElement(name = "TitoliAccessoIVAPreassolta")
    protected List<TitoliAccessoIVAPreassolta> titoliAccessoIVAPreassolta;
    @XmlElement(name = "TitoliIVAPreassoltaAnnullati")
    protected List<TitoliIVAPreassoltaAnnullati> titoliIVAPreassoltaAnnullati;
    @XmlElement(name = "BigliettiAbbonamento")
    protected List<BigliettiAbbonamento> bigliettiAbbonamento;
    @XmlElement(name = "BigliettiAbbonamentoAnnullati")
    protected List<BigliettiAbbonamentoAnnullati> bigliettiAbbonamentoAnnullati;

    /**
     * Recupera il valore della proprietà codiceOrdine.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCodiceOrdine() {
        return codiceOrdine;
    }

    /**
     * Imposta il valore della proprietà codiceOrdine.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCodiceOrdine(String value) {
        this.codiceOrdine = value;
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
     * Gets the value of the titoliAccesso property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the titoliAccesso property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getTitoliAccesso().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link TitoliAccesso }
     * 
     * 
     */
    public List<TitoliAccesso> getTitoliAccesso() {
        if (titoliAccesso == null) {
            titoliAccesso = new ArrayList<TitoliAccesso>();
        }
        return this.titoliAccesso;
    }

    /**
     * Gets the value of the titoliAnnullati property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the titoliAnnullati property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getTitoliAnnullati().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link TitoliAnnullati }
     * 
     * 
     */
    public List<TitoliAnnullati> getTitoliAnnullati() {
        if (titoliAnnullati == null) {
            titoliAnnullati = new ArrayList<TitoliAnnullati>();
        }
        return this.titoliAnnullati;
    }

    /**
     * Gets the value of the titoliAccessoIVAPreassolta property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the titoliAccessoIVAPreassolta property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getTitoliAccessoIVAPreassolta().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link TitoliAccessoIVAPreassolta }
     * 
     * 
     */
    public List<TitoliAccessoIVAPreassolta> getTitoliAccessoIVAPreassolta() {
        if (titoliAccessoIVAPreassolta == null) {
            titoliAccessoIVAPreassolta = new ArrayList<TitoliAccessoIVAPreassolta>();
        }
        return this.titoliAccessoIVAPreassolta;
    }

    /**
     * Gets the value of the titoliIVAPreassoltaAnnullati property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the titoliIVAPreassoltaAnnullati property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getTitoliIVAPreassoltaAnnullati().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link TitoliIVAPreassoltaAnnullati }
     * 
     * 
     */
    public List<TitoliIVAPreassoltaAnnullati> getTitoliIVAPreassoltaAnnullati() {
        if (titoliIVAPreassoltaAnnullati == null) {
            titoliIVAPreassoltaAnnullati = new ArrayList<TitoliIVAPreassoltaAnnullati>();
        }
        return this.titoliIVAPreassoltaAnnullati;
    }

    /**
     * Gets the value of the bigliettiAbbonamento property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the bigliettiAbbonamento property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getBigliettiAbbonamento().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link BigliettiAbbonamento }
     * 
     * 
     */
    public List<BigliettiAbbonamento> getBigliettiAbbonamento() {
        if (bigliettiAbbonamento == null) {
            bigliettiAbbonamento = new ArrayList<BigliettiAbbonamento>();
        }
        return this.bigliettiAbbonamento;
    }

    /**
     * Gets the value of the bigliettiAbbonamentoAnnullati property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the bigliettiAbbonamentoAnnullati property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getBigliettiAbbonamentoAnnullati().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link BigliettiAbbonamentoAnnullati }
     * 
     * 
     */
    public List<BigliettiAbbonamentoAnnullati> getBigliettiAbbonamentoAnnullati() {
        if (bigliettiAbbonamentoAnnullati == null) {
            bigliettiAbbonamentoAnnullati = new ArrayList<BigliettiAbbonamentoAnnullati>();
        }
        return this.bigliettiAbbonamentoAnnullati;
    }

}
