//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.11.18 alle 05:15:26 PM CET 
//


package cnr.isti.sse.big.data.reply.log;

import java.math.BigInteger;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;

import org.apache.commons.lang3.tuple.ImmutableTriple;


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
 *         &lt;element name="NProgressivi" type="{http://www.w3.org/2001/XMLSchema}integer"/>
 *         &lt;element name="CorrispettivoLordo" type="{http://www.w3.org/2001/XMLSchema}integer"/>
 *         &lt;element name="PrevenditaLordo" type="{http://www.w3.org/2001/XMLSchema}integer"/>
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
    "nProgressivi",
    "corrispettivoLordo",
    "prevenditaLordo"
})
@XmlRootElement(name = "Log")
public class Log {

    @XmlElement(name = "NProgressivi", required = true)
    protected BigInteger nProgressivi;
    @XmlElement(name = "CorrispettivoLordo", required = true)
    protected BigInteger corrispettivoLordo;
    @XmlElement(name = "PrevenditaLordo", required = true)
    protected BigInteger prevenditaLordo;

    
    public Log(ImmutableTriple<Integer, Integer, Integer> imm){
    	nProgressivi = BigInteger.valueOf(imm.left);
    	corrispettivoLordo  = BigInteger.valueOf(imm.middle);
    	prevenditaLordo  = BigInteger.valueOf(imm.right);
    }
    /**
     * Recupera il valore della proprietà nProgressivi.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getNProgressivi() {
        return nProgressivi;
    }

    /**
     * Imposta il valore della proprietà nProgressivi.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setNProgressivi(BigInteger value) {
        this.nProgressivi = value;
    }

    /**
     * Recupera il valore della proprietà corrispettivoLordo.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getCorrispettivoLordo() {
        return corrispettivoLordo;
    }

    /**
     * Imposta il valore della proprietà corrispettivoLordo.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setCorrispettivoLordo(BigInteger value) {
        this.corrispettivoLordo = value;
    }

    /**
     * Recupera il valore della proprietà prevenditaLordo.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getPrevenditaLordo() {
        return prevenditaLordo;
    }

    /**
     * Imposta il valore della proprietà prevenditaLordo.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setPrevenditaLordo(BigInteger value) {
        this.prevenditaLordo = value;
    }

	@Override
	public String toString() {
		return (nProgressivi != null ? "nProgressivi: " + nProgressivi + ", " : "")
				+ (corrispettivoLordo != null ? "corrispettivoLordo: " + corrispettivoLordo + ",  " : "")
				+ (prevenditaLordo != null ? "prevenditaLordo: " + prevenditaLordo : "");
	}
    
    

}
