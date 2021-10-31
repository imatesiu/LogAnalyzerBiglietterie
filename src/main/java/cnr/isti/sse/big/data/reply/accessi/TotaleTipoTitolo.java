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
 *         &lt;element ref="{http://tempuri.org/accessi}TipoTitolo"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliLTA"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliNoAccessoTradiz"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliNoAccessoDigitali"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliAutomatizzatiTradiz"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliAutomatizzatiDigitali"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliManualiTradiz"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliManualiDigitali"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliAnnullatiTradiz"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliAnnullatiDigitali"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliDaspatiTradiz"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliDaspatiDigitali"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliRubatiTradiz"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliRubatiDigitali"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliBLTradiz"/>
 *         &lt;element ref="{http://tempuri.org/accessi}TotaleTitoliBLDigitali"/>
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
    "tipoTitolo",
    "totaleTitoliLTA",
    "totaleTitoliNoAccessoTradiz",
    "totaleTitoliNoAccessoDigitali",
    "totaleTitoliAutomatizzatiTradiz",
    "totaleTitoliAutomatizzatiDigitali",
    "totaleTitoliManualiTradiz",
    "totaleTitoliManualiDigitali",
    "totaleTitoliAnnullatiTradiz",
    "totaleTitoliAnnullatiDigitali",
    "totaleTitoliDaspatiTradiz",
    "totaleTitoliDaspatiDigitali",
    "totaleTitoliRubatiTradiz",
    "totaleTitoliRubatiDigitali",
    "totaleTitoliBLTradiz",
    "totaleTitoliBLDigitali"
})
@XmlRootElement(name = "TotaleTipoTitolo")
public class TotaleTipoTitolo {

    @XmlElement(name = "TipoTitolo", required = true)
    protected String tipoTitolo;
    @XmlElement(name = "TotaleTitoliLTA", required = true)
    protected String totaleTitoliLTA;
    @XmlElement(name = "TotaleTitoliNoAccessoTradiz", required = true)
    protected String totaleTitoliNoAccessoTradiz;
    @XmlElement(name = "TotaleTitoliNoAccessoDigitali", required = true)
    protected String totaleTitoliNoAccessoDigitali;
    @XmlElement(name = "TotaleTitoliAutomatizzatiTradiz", required = true)
    protected String totaleTitoliAutomatizzatiTradiz;
    @XmlElement(name = "TotaleTitoliAutomatizzatiDigitali", required = true)
    protected String totaleTitoliAutomatizzatiDigitali;
    @XmlElement(name = "TotaleTitoliManualiTradiz", required = true)
    protected String totaleTitoliManualiTradiz;
    @XmlElement(name = "TotaleTitoliManualiDigitali", required = true)
    protected String totaleTitoliManualiDigitali;
    @XmlElement(name = "TotaleTitoliAnnullatiTradiz", required = true)
    protected String totaleTitoliAnnullatiTradiz;
    @XmlElement(name = "TotaleTitoliAnnullatiDigitali", required = true)
    protected String totaleTitoliAnnullatiDigitali;
    @XmlElement(name = "TotaleTitoliDaspatiTradiz", required = true)
    protected String totaleTitoliDaspatiTradiz;
    @XmlElement(name = "TotaleTitoliDaspatiDigitali", required = true)
    protected String totaleTitoliDaspatiDigitali;
    @XmlElement(name = "TotaleTitoliRubatiTradiz", required = true)
    protected String totaleTitoliRubatiTradiz;
    @XmlElement(name = "TotaleTitoliRubatiDigitali", required = true)
    protected String totaleTitoliRubatiDigitali;
    @XmlElement(name = "TotaleTitoliBLTradiz", required = true)
    protected String totaleTitoliBLTradiz;
    @XmlElement(name = "TotaleTitoliBLDigitali", required = true)
    protected String totaleTitoliBLDigitali;

    /**
     * Recupera il valore della proprietà tipoTitolo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTipoTitolo() {
        return tipoTitolo;
    }

    /**
     * Imposta il valore della proprietà tipoTitolo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTipoTitolo(String value) {
        this.tipoTitolo = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliLTA.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliLTA() {
        return totaleTitoliLTA;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliLTA.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliLTA(String value) {
        this.totaleTitoliLTA = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliNoAccessoTradiz.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliNoAccessoTradiz() {
        return totaleTitoliNoAccessoTradiz;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliNoAccessoTradiz.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliNoAccessoTradiz(String value) {
        this.totaleTitoliNoAccessoTradiz = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliNoAccessoDigitali.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliNoAccessoDigitali() {
        return totaleTitoliNoAccessoDigitali;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliNoAccessoDigitali.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliNoAccessoDigitali(String value) {
        this.totaleTitoliNoAccessoDigitali = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliAutomatizzatiTradiz.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliAutomatizzatiTradiz() {
        return totaleTitoliAutomatizzatiTradiz;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliAutomatizzatiTradiz.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliAutomatizzatiTradiz(String value) {
        this.totaleTitoliAutomatizzatiTradiz = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliAutomatizzatiDigitali.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliAutomatizzatiDigitali() {
        return totaleTitoliAutomatizzatiDigitali;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliAutomatizzatiDigitali.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliAutomatizzatiDigitali(String value) {
        this.totaleTitoliAutomatizzatiDigitali = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliManualiTradiz.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliManualiTradiz() {
        return totaleTitoliManualiTradiz;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliManualiTradiz.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliManualiTradiz(String value) {
        this.totaleTitoliManualiTradiz = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliManualiDigitali.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliManualiDigitali() {
        return totaleTitoliManualiDigitali;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliManualiDigitali.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliManualiDigitali(String value) {
        this.totaleTitoliManualiDigitali = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliAnnullatiTradiz.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliAnnullatiTradiz() {
        return totaleTitoliAnnullatiTradiz;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliAnnullatiTradiz.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliAnnullatiTradiz(String value) {
        this.totaleTitoliAnnullatiTradiz = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliAnnullatiDigitali.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliAnnullatiDigitali() {
        return totaleTitoliAnnullatiDigitali;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliAnnullatiDigitali.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliAnnullatiDigitali(String value) {
        this.totaleTitoliAnnullatiDigitali = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliDaspatiTradiz.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliDaspatiTradiz() {
        return totaleTitoliDaspatiTradiz;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliDaspatiTradiz.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliDaspatiTradiz(String value) {
        this.totaleTitoliDaspatiTradiz = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliDaspatiDigitali.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliDaspatiDigitali() {
        return totaleTitoliDaspatiDigitali;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliDaspatiDigitali.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliDaspatiDigitali(String value) {
        this.totaleTitoliDaspatiDigitali = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliRubatiTradiz.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliRubatiTradiz() {
        return totaleTitoliRubatiTradiz;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliRubatiTradiz.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliRubatiTradiz(String value) {
        this.totaleTitoliRubatiTradiz = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliRubatiDigitali.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliRubatiDigitali() {
        return totaleTitoliRubatiDigitali;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliRubatiDigitali.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliRubatiDigitali(String value) {
        this.totaleTitoliRubatiDigitali = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliBLTradiz.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliBLTradiz() {
        return totaleTitoliBLTradiz;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliBLTradiz.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliBLTradiz(String value) {
        this.totaleTitoliBLTradiz = value;
    }

    /**
     * Recupera il valore della proprietà totaleTitoliBLDigitali.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTotaleTitoliBLDigitali() {
        return totaleTitoliBLDigitali;
    }

    /**
     * Imposta il valore della proprietà totaleTitoliBLDigitali.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTotaleTitoliBLDigitali(String value) {
        this.totaleTitoliBLDigitali = value;
    }

	@Override
	public String toString() {
		return (tipoTitolo != null ? "tipoTitolo: " + tipoTitolo + ", \\n " : "")
				+ (totaleTitoliLTA != null ? "totaleTitoliLTA: " + totaleTitoliLTA + ", \\n " : "")
				+ (totaleTitoliNoAccessoTradiz != null
						? "totaleTitoliNoAccessoTradiz: " + totaleTitoliNoAccessoTradiz + ", \\n "
						: "")
				+ (totaleTitoliNoAccessoDigitali != null
						? "totaleTitoliNoAccessoDigitali: " + totaleTitoliNoAccessoDigitali + ", \\n "
						: "")
				+ (totaleTitoliAutomatizzatiTradiz != null
						? "totaleTitoliAutomatizzatiTradiz: " + totaleTitoliAutomatizzatiTradiz + ", \\n "
						: "")
				+ (totaleTitoliAutomatizzatiDigitali != null
						? "totaleTitoliAutomatizzatiDigitali: " + totaleTitoliAutomatizzatiDigitali + ", \\n "
						: "")
				+ (totaleTitoliManualiTradiz != null
						? "totaleTitoliManualiTradiz: " + totaleTitoliManualiTradiz + ", \\n "
						: "")
				+ (totaleTitoliManualiDigitali != null
						? "totaleTitoliManualiDigitali: " + totaleTitoliManualiDigitali + ", \\n "
						: "")
				+ (totaleTitoliAnnullatiTradiz != null
						? "totaleTitoliAnnullatiTradiz: " + totaleTitoliAnnullatiTradiz + ", \\n "
						: "")
				+ (totaleTitoliAnnullatiDigitali != null
						? "totaleTitoliAnnullatiDigitali: " + totaleTitoliAnnullatiDigitali + ", \\n "
						: "")
				+ (totaleTitoliDaspatiTradiz != null
						? "totaleTitoliDaspatiTradiz: " + totaleTitoliDaspatiTradiz + ", \\n "
						: "")
				+ (totaleTitoliDaspatiDigitali != null
						? "totaleTitoliDaspatiDigitali: " + totaleTitoliDaspatiDigitali + ", \\n "
						: "")
				+ (totaleTitoliRubatiTradiz != null ? "totaleTitoliRubatiTradiz: " + totaleTitoliRubatiTradiz + ", \\n "
						: "")
				+ (totaleTitoliRubatiDigitali != null
						? "totaleTitoliRubatiDigitali: " + totaleTitoliRubatiDigitali + ", \\n "
						: "")
				+ (totaleTitoliBLTradiz != null ? "totaleTitoliBLTradiz: " + totaleTitoliBLTradiz + ", \\n " : "")
				+ (totaleTitoliBLDigitali != null ? "totaleTitoliBLDigitali: " + totaleTitoliBLDigitali : "");
	}
    
    

}
