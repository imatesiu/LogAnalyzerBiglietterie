//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.11.18 alle 08:39:48 PM CET 
//


package cnr.isti.sse.big.data.reply.accessi;

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
 *         &lt;element ref="{http://tempuri.org/accessi}TipoTitoloAbbonamento"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliAbbLTA"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliAbbNoAccessoTradiz"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliAbbNoAccessoDigitali"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliAbbAutomatizzatiTradiz"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliAbbAutomatizzatiDigitali"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliAbbManualiTradiz"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliAbbManualiDigitali"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliAbbAnnullatiTradiz"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliAbbAnnullatiDigitali"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliAbbDaspatiTradiz"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliAbbDaspatiDigitali"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliAbbRubatiTradiz"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliAbbRubatiDigitali"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliAbbBLTradiz"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliAbbBLDigitali"/>
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
    "tipoTitoloAbbonamento",
    "totaleTitoliAbbLTA",
    "totaleTitoliAbbNoAccessoTradiz",
    "totaleTitoliAbbNoAccessoDigitali",
    "totaleTitoliAbbAutomatizzatiTradiz",
    "totaleTitoliAbbAutomatizzatiDigitali",
    "totaleTitoliAbbManualiTradiz",
    "totaleTitoliAbbManualiDigitali",
    "totaleTitoliAbbAnnullatiTradiz",
    "totaleTitoliAbbAnnullatiDigitali",
    "totaleTitoliAbbDaspatiTradiz",
    "totaleTitoliAbbDaspatiDigitali",
    "totaleTitoliAbbRubatiTradiz",
    "totaleTitoliAbbRubatiDigitali",
    "totaleTitoliAbbBLTradiz",
    "totaleTitoliAbbBLDigitali"
})
@XmlRootElement(name = "TotaleTipoTitoloAbbonamento")
public class TotaleTipoTitoloAbbonamento {

    @XmlElement(name = "TipoTitoloAbbonamento", required = true)
    protected String tipoTitoloAbbonamento;
    @XmlElement(name = "TotaleTitoliAbbLTA", required = true)
    protected String totaleTitoliAbbLTA;
    @XmlElement(name = "TotaleTitoliAbbNoAccessoTradiz", required = true)
    protected String totaleTitoliAbbNoAccessoTradiz;
    @XmlElement(name = "TotaleTitoliAbbNoAccessoDigitali", required = true)
    protected String totaleTitoliAbbNoAccessoDigitali;
    @XmlElement(name = "TotaleTitoliAbbAutomatizzatiTradiz", required = true)
    protected String totaleTitoliAbbAutomatizzatiTradiz;
    @XmlElement(name = "TotaleTitoliAbbAutomatizzatiDigitali", required = true)
    protected String totaleTitoliAbbAutomatizzatiDigitali;
    @XmlElement(name = "TotaleTitoliAbbManualiTradiz", required = true)
    protected String totaleTitoliAbbManualiTradiz;
    @XmlElement(name = "TotaleTitoliAbbManualiDigitali", required = true)
    protected String totaleTitoliAbbManualiDigitali;
    @XmlElement(name = "TotaleTitoliAbbAnnullatiTradiz", required = true)
    protected String totaleTitoliAbbAnnullatiTradiz;
    @XmlElement(name = "TotaleTitoliAbbAnnullatiDigitali", required = true)
    protected String totaleTitoliAbbAnnullatiDigitali;
    @XmlElement(name = "TotaleTitoliAbbDaspatiTradiz", required = true)
    protected String totaleTitoliAbbDaspatiTradiz;
    @XmlElement(name = "TotaleTitoliAbbDaspatiDigitali", required = true)
    protected String totaleTitoliAbbDaspatiDigitali;
    @XmlElement(name = "TotaleTitoliAbbRubatiTradiz", required = true)
    protected String totaleTitoliAbbRubatiTradiz;
    @XmlElement(name = "TotaleTitoliAbbRubatiDigitali", required = true)
    protected String totaleTitoliAbbRubatiDigitali;
    @XmlElement(name = "TotaleTitoliAbbBLTradiz", required = true)
    protected String totaleTitoliAbbBLTradiz;
    @XmlElement(name = "TotaleTitoliAbbBLDigitali", required = true)
    protected String totaleTitoliAbbBLDigitali;

    /**
     * Recupera il valore della proprietà tipoTitoloAbbonamento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTipoTitoloAbbonamento() {
        return tipoTitoloAbbonamento;
    }

    /**
     * Imposta il valore della proprietà tipoTitoloAbbonamento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTipoTitoloAbbonamento(String value) {
        this.tipoTitoloAbbonamento = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliAbbLTA.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliAbbLTA() {
        return totaleTitoliAbbLTA;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliAbbLTA.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliAbbLTA(String value) {
        this.totaleTitoliAbbLTA = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliAbbNoAccessoTradiz.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliAbbNoAccessoTradiz() {
        return totaleTitoliAbbNoAccessoTradiz;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliAbbNoAccessoTradiz.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliAbbNoAccessoTradiz(String value) {
        this.totaleTitoliAbbNoAccessoTradiz = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliAbbNoAccessoDigitali.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliAbbNoAccessoDigitali() {
        return totaleTitoliAbbNoAccessoDigitali;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliAbbNoAccessoDigitali.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliAbbNoAccessoDigitali(String value) {
        this.totaleTitoliAbbNoAccessoDigitali = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliAbbAutomatizzatiTradiz.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliAbbAutomatizzatiTradiz() {
        return totaleTitoliAbbAutomatizzatiTradiz;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliAbbAutomatizzatiTradiz.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliAbbAutomatizzatiTradiz(String value) {
        this.totaleTitoliAbbAutomatizzatiTradiz = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliAbbAutomatizzatiDigitali.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliAbbAutomatizzatiDigitali() {
        return totaleTitoliAbbAutomatizzatiDigitali;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliAbbAutomatizzatiDigitali.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliAbbAutomatizzatiDigitali(String value) {
        this.totaleTitoliAbbAutomatizzatiDigitali = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliAbbManualiTradiz.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliAbbManualiTradiz() {
        return totaleTitoliAbbManualiTradiz;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliAbbManualiTradiz.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliAbbManualiTradiz(String value) {
        this.totaleTitoliAbbManualiTradiz = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliAbbManualiDigitali.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliAbbManualiDigitali() {
        return totaleTitoliAbbManualiDigitali;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliAbbManualiDigitali.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliAbbManualiDigitali(String value) {
        this.totaleTitoliAbbManualiDigitali = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliAbbAnnullatiTradiz.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliAbbAnnullatiTradiz() {
        return totaleTitoliAbbAnnullatiTradiz;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliAbbAnnullatiTradiz.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliAbbAnnullatiTradiz(String value) {
        this.totaleTitoliAbbAnnullatiTradiz = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliAbbAnnullatiDigitali.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliAbbAnnullatiDigitali() {
        return totaleTitoliAbbAnnullatiDigitali;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliAbbAnnullatiDigitali.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliAbbAnnullatiDigitali(String value) {
        this.totaleTitoliAbbAnnullatiDigitali = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliAbbDaspatiTradiz.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliAbbDaspatiTradiz() {
        return totaleTitoliAbbDaspatiTradiz;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliAbbDaspatiTradiz.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliAbbDaspatiTradiz(String value) {
        this.totaleTitoliAbbDaspatiTradiz = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliAbbDaspatiDigitali.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliAbbDaspatiDigitali() {
        return totaleTitoliAbbDaspatiDigitali;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliAbbDaspatiDigitali.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliAbbDaspatiDigitali(String value) {
        this.totaleTitoliAbbDaspatiDigitali = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliAbbRubatiTradiz.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliAbbRubatiTradiz() {
        return totaleTitoliAbbRubatiTradiz;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliAbbRubatiTradiz.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliAbbRubatiTradiz(String value) {
        this.totaleTitoliAbbRubatiTradiz = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliAbbRubatiDigitali.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliAbbRubatiDigitali() {
        return totaleTitoliAbbRubatiDigitali;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliAbbRubatiDigitali.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliAbbRubatiDigitali(String value) {
        this.totaleTitoliAbbRubatiDigitali = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliAbbBLTradiz.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliAbbBLTradiz() {
        return totaleTitoliAbbBLTradiz;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliAbbBLTradiz.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliAbbBLTradiz(String value) {
        this.totaleTitoliAbbBLTradiz = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliAbbBLDigitali.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliAbbBLDigitali() {
        return totaleTitoliAbbBLDigitali;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliAbbBLDigitali.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliAbbBLDigitali(String value) {
        this.totaleTitoliAbbBLDigitali = value;
    }

}
