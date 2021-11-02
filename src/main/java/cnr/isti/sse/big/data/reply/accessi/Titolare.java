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
 *         &lt;element ref="{http://tempuri.org/accessi}DenominazioneTitolareCA"/>
 *         &lt;element ref="{http://tempuri.org/accessi}CFTitolareCA"/>
 *         &lt;element ref="{http://tempuri.org/accessi}CodiceSistemaCA"/>
 *         &lt;element ref="{http://tempuri.org/accessi}DataRiepilogo"/>
 *         &lt;element ref="{http://tempuri.org/accessi}DataGenerazioneRiepilogo"/>
 *         &lt;element ref="{http://tempuri.org/accessi}OraGenerazioneRiepilogo"/>
 *         &lt;element ref="{http://tempuri.org/accessi}ProgressivoRiepilogo"/>
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
    "denominazioneTitolareCA",
    "cfTitolareCA",
    "codiceSistemaCA",
    "dataRiepilogo",
    "dataGenerazioneRiepilogo",
    "oraGenerazioneRiepilogo",
    "progressivoRiepilogo"
})
@XmlRootElement(name = "Titolare")
public class Titolare {

    @XmlElement(name = "DenominazioneTitolareCA", required = true)
    protected String denominazioneTitolareCA;
    @XmlElement(name = "CFTitolareCA", required = true)
    protected String cfTitolareCA;
    @XmlElement(name = "CodiceSistemaCA", required = true)
    protected String codiceSistemaCA;
    @XmlElement(name = "DataRiepilogo", required = true)
    protected String dataRiepilogo;
    @XmlElement(name = "DataGenerazioneRiepilogo", required = true)
    protected String dataGenerazioneRiepilogo;
    @XmlElement(name = "OraGenerazioneRiepilogo", required = true)
    protected String oraGenerazioneRiepilogo;
    @XmlElement(name = "ProgressivoRiepilogo", required = true)
    protected String progressivoRiepilogo;

    /**
     * Recupera il valore della proprietà denominazioneTitolareCA.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDenominazioneTitolareCA() {
        return denominazioneTitolareCA;
    }

    /**
     * Imposta il valore della proprietà denominazioneTitolareCA.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDenominazioneTitolareCA(String value) {
        this.denominazioneTitolareCA = value;
    }

    /**
     * Recupera il valore della proprietà cfTitolareCA.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCFTitolareCA() {
        return cfTitolareCA;
    }

    /**
     * Imposta il valore della proprietà cfTitolareCA.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCFTitolareCA(String value) {
        this.cfTitolareCA = value;
    }

    /**
     * Recupera il valore della proprietà codiceSistemaCA.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCodiceSistemaCA() {
        return codiceSistemaCA;
    }

    /**
     * Imposta il valore della proprietà codiceSistemaCA.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCodiceSistemaCA(String value) {
        this.codiceSistemaCA = value;
    }

    /**
     * Recupera il valore della proprietà dataRiepilogo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDataRiepilogo() {
        return dataRiepilogo;
    }

    /**
     * Imposta il valore della proprietà dataRiepilogo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDataRiepilogo(String value) {
        this.dataRiepilogo = value;
    }

    /**
     * Recupera il valore della proprietà dataGenerazioneRiepilogo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDataGenerazioneRiepilogo() {
        return dataGenerazioneRiepilogo;
    }

    /**
     * Imposta il valore della proprietà dataGenerazioneRiepilogo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDataGenerazioneRiepilogo(String value) {
        this.dataGenerazioneRiepilogo = value;
    }

    /**
     * Recupera il valore della proprietà oraGenerazioneRiepilogo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getOraGenerazioneRiepilogo() {
        return oraGenerazioneRiepilogo;
    }

    /**
     * Imposta il valore della proprietà oraGenerazioneRiepilogo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setOraGenerazioneRiepilogo(String value) {
        this.oraGenerazioneRiepilogo = value;
    }

    /**
     * Recupera il valore della proprietà progressivoRiepilogo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getProgressivoRiepilogo() {
        return progressivoRiepilogo;
    }

    /**
     * Imposta il valore della proprietà progressivoRiepilogo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setProgressivoRiepilogo(String value) {
        this.progressivoRiepilogo = value;
    }

	@Override
	public String toString() {
		return (denominazioneTitolareCA != null ? "denominazioneTitolareCA: " + denominazioneTitolareCA + ", \\n " : "")
				+ (cfTitolareCA != null ? "cfTitolareCA: " + cfTitolareCA + ", \\n " : "")
				+ (codiceSistemaCA != null ? "codiceSistemaCA: " + codiceSistemaCA + ", \\n " : "")
				+ (dataRiepilogo != null ? "dataRiepilogo: " + dataRiepilogo + ", \\n " : "")
				+ (dataGenerazioneRiepilogo != null ? "dataGenerazioneRiepilogo: " + dataGenerazioneRiepilogo + ", \\n "
						: "")
				+ (oraGenerazioneRiepilogo != null ? "oraGenerazioneRiepilogo: " + oraGenerazioneRiepilogo + ", \\n "
						: "")
				+ (progressivoRiepilogo != null ? "progressivoRiepilogo: " + progressivoRiepilogo : "\n");
	}

    
}
