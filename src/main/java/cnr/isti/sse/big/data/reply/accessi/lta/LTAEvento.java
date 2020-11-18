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
 *         &lt;element ref="{http://tempuri.org/lta}Supporto" maxOccurs="unbounded"/>
 *         &lt;element ref="{http://tempuri.org/lta}TitoloAccesso" maxOccurs="unbounded" minOccurs="0"/>
 *       &lt;/sequence>
 *       &lt;attribute name="CFOrganizzatore" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CodiceLocale" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="DataEvento" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="OraEvento" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="Titolo" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="TipoGenere" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="DataApertura" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="OraApertura" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "supporto",
    "titoloAccesso"
})
@XmlRootElement(name = "LTA_Evento")
public class LTAEvento {

    @XmlElement(name = "Supporto", required = true)
    protected List<Supporto> supporto;
    @XmlElement(name = "TitoloAccesso")
    protected List<TitoloAccesso> titoloAccesso;
    @XmlAttribute(name = "CFOrganizzatore", required = true)
    protected String cfOrganizzatore;
    @XmlAttribute(name = "CodiceLocale", required = true)
    protected String codiceLocale;
    @XmlAttribute(name = "DataEvento", required = true)
    protected String dataEvento;
    @XmlAttribute(name = "OraEvento", required = true)
    protected String oraEvento;
    @XmlAttribute(name = "Titolo", required = true)
    protected String titolo;
    @XmlAttribute(name = "TipoGenere", required = true)
    protected String tipoGenere;
    @XmlAttribute(name = "DataApertura", required = true)
    protected String dataApertura;
    @XmlAttribute(name = "OraApertura", required = true)
    protected String oraApertura;

    /**
     * Gets the value of the supporto property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the supporto property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getSupporto().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link Supporto }
     * 
     * 
     */
    public List<Supporto> getSupporto() {
        if (supporto == null) {
            supporto = new ArrayList<Supporto>();
        }
        return this.supporto;
    }

    /**
     * Gets the value of the titoloAccesso property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the titoloAccesso property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getTitoloAccesso().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link TitoloAccesso }
     * 
     * 
     */
    public List<TitoloAccesso> getTitoloAccesso() {
        if (titoloAccesso == null) {
            titoloAccesso = new ArrayList<TitoloAccesso>();
        }
        return this.titoloAccesso;
    }

    /**
     * Recupera il valore della proprietà cfOrganizzatore.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCFOrganizzatore() {
        return cfOrganizzatore;
    }

    /**
     * Imposta il valore della proprietà cfOrganizzatore.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCFOrganizzatore(String value) {
        this.cfOrganizzatore = value;
    }

    /**
     * Recupera il valore della proprietà codiceLocale.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCodiceLocale() {
        return codiceLocale;
    }

    /**
     * Imposta il valore della proprietà codiceLocale.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCodiceLocale(String value) {
        this.codiceLocale = value;
    }

    /**
     * Recupera il valore della proprietà dataEvento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDataEvento() {
        return dataEvento;
    }

    /**
     * Imposta il valore della proprietà dataEvento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDataEvento(String value) {
        this.dataEvento = value;
    }

    /**
     * Recupera il valore della proprietà oraEvento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getOraEvento() {
        return oraEvento;
    }

    /**
     * Imposta il valore della proprietà oraEvento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setOraEvento(String value) {
        this.oraEvento = value;
    }

    /**
     * Recupera il valore della proprietà titolo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTitolo() {
        return titolo;
    }

    /**
     * Imposta il valore della proprietà titolo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTitolo(String value) {
        this.titolo = value;
    }

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
     * Recupera il valore della proprietà dataApertura.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDataApertura() {
        return dataApertura;
    }

    /**
     * Imposta il valore della proprietà dataApertura.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDataApertura(String value) {
        this.dataApertura = value;
    }

    /**
     * Recupera il valore della proprietà oraApertura.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getOraApertura() {
        return oraApertura;
    }

    /**
     * Imposta il valore della proprietà oraApertura.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setOraApertura(String value) {
        this.oraApertura = value;
    }

}
