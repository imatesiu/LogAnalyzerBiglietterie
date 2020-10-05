//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.10.05 alle 12:50:22 PM CEST 
//


package cnr.isti.sse.big.data.transazioni;

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
 *         &lt;element ref="{}OriginaleRiferimentoAnnullamento"/>
 *         &lt;element ref="{}CartaRiferimentoAnnullamento"/>
 *         &lt;element ref="{}CausaleRiferimentoAnnullamento"/>
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
    "originaleRiferimentoAnnullamento",
    "cartaRiferimentoAnnullamento",
    "causaleRiferimentoAnnullamento"
})
@XmlRootElement(name = "RiferimentoAnnullamento")
public class RiferimentoAnnullamento {

    @XmlElement(name = "OriginaleRiferimentoAnnullamento", required = true)
    protected String originaleRiferimentoAnnullamento;
    @XmlElement(name = "CartaRiferimentoAnnullamento", required = true)
    protected String cartaRiferimentoAnnullamento;
    @XmlElement(name = "CausaleRiferimentoAnnullamento", required = true)
    protected String causaleRiferimentoAnnullamento;

    /**
     * Recupera il valore della proprietà originaleRiferimentoAnnullamento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getOriginaleRiferimentoAnnullamento() {
        return originaleRiferimentoAnnullamento;
    }

    /**
     * Imposta il valore della proprietà originaleRiferimentoAnnullamento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setOriginaleRiferimentoAnnullamento(String value) {
        this.originaleRiferimentoAnnullamento = value;
    }

    /**
     * Recupera il valore della proprietà cartaRiferimentoAnnullamento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCartaRiferimentoAnnullamento() {
        return cartaRiferimentoAnnullamento;
    }

    /**
     * Imposta il valore della proprietà cartaRiferimentoAnnullamento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCartaRiferimentoAnnullamento(String value) {
        this.cartaRiferimentoAnnullamento = value;
    }

    /**
     * Recupera il valore della proprietà causaleRiferimentoAnnullamento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCausaleRiferimentoAnnullamento() {
        return causaleRiferimentoAnnullamento;
    }

    /**
     * Imposta il valore della proprietà causaleRiferimentoAnnullamento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCausaleRiferimentoAnnullamento(String value) {
        this.causaleRiferimentoAnnullamento = value;
    }

}
