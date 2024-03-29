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
 *         &lt;element ref="{http://siae.it/mensile}Denominazione"/>
 *         &lt;element ref="{http://siae.it/mensile}CodiceFiscale"/>
 *         &lt;element ref="{http://siae.it/mensile}TipoOrganizzatore"/>
 *         &lt;element ref="{http://siae.it/mensile}Evento" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element ref="{http://siae.it/mensile}Abbonamenti" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element ref="{http://siae.it/mensile}AltriProventiGenerici" maxOccurs="unbounded" minOccurs="0"/>
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
    "denominazione",
    "codiceFiscale",
    "tipoOrganizzatore",
    "evento",
    "abbonamenti",
    "altriProventiGenerici"
})
@XmlRootElement(name = "Organizzatore")
public class Organizzatore {

    @XmlElement(name = "Denominazione", required = true)
    protected String denominazione;
    @XmlElement(name = "CodiceFiscale", required = true)
    protected String codiceFiscale;
    @XmlElement(name = "TipoOrganizzatore", required = true)
    protected TipoOrganizzatore tipoOrganizzatore;
    @XmlElement(name = "Evento")
    protected List<Evento> evento;
    @XmlElement(name = "Abbonamenti")
    protected List<Abbonamenti> abbonamenti;
    @XmlElement(name = "AltriProventiGenerici")
    protected List<AltriProventiGenerici> altriProventiGenerici;

    /**
     * Recupera il valore della proprietà denominazione.
     * 
     * @return
     *     possible object is
     *     {@link Denominazione }
     *     
     */
    public String getDenominazione() {
        return denominazione;
    }

    /**
     * Imposta il valore della proprietà denominazione.
     * 
     * @param value
     *     allowed object is
     *     {@link Denominazione }
     *     
     */
    public void setDenominazione(String value) {
        this.denominazione = value;
    }

    /**
     * Recupera il valore della proprietà codiceFiscale.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCodiceFiscale() {
        return codiceFiscale;
    }

    /**
     * Imposta il valore della proprietà codiceFiscale.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCodiceFiscale(String value) {
        this.codiceFiscale = value;
    }

    /**
     * Recupera il valore della proprietà tipoOrganizzatore.
     * 
     * @return
     *     possible object is
     *     {@link TipoOrganizzatore }
     *     
     */
    public TipoOrganizzatore getTipoOrganizzatore() {
        return tipoOrganizzatore;
    }

    /**
     * Imposta il valore della proprietà tipoOrganizzatore.
     * 
     * @param value
     *     allowed object is
     *     {@link TipoOrganizzatore }
     *     
     */
    public void setTipoOrganizzatore(TipoOrganizzatore value) {
        this.tipoOrganizzatore = value;
    }

    /**
     * Gets the value of the evento property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the evento property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getEvento().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link Evento }
     * 
     * 
     */
    public List<Evento> getEvento() {
        if (evento == null) {
            evento = new ArrayList<Evento>();
        }
        return this.evento;
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

    /**
     * Gets the value of the altriProventiGenerici property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the altriProventiGenerici property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getAltriProventiGenerici().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link AltriProventiGenerici }
     * 
     * 
     */
    public List<AltriProventiGenerici> getAltriProventiGenerici() {
        if (altriProventiGenerici == null) {
            altriProventiGenerici = new ArrayList<AltriProventiGenerici>();
        }
        return this.altriProventiGenerici;
    }

}
