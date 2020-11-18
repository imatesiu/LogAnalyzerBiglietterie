//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.11.18 alle 10:56:34 PM CET 
//


package cnr.isti.sse.big.data.reply.accessi.lta;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
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
 *       &lt;attribute name="TipoSupportoId" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CodSupportoId" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "")
@XmlRootElement(name = "Supporto")
public class Supporto {

    @XmlAttribute(name = "TipoSupportoId", required = true)
    protected String tipoSupportoId;
    @XmlAttribute(name = "CodSupportoId", required = true)
    protected String codSupportoId;

    /**
     * Recupera il valore della proprietà tipoSupportoId.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTipoSupportoId() {
        return tipoSupportoId;
    }

    /**
     * Imposta il valore della proprietà tipoSupportoId.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTipoSupportoId(String value) {
        this.tipoSupportoId = value;
    }

    /**
     * Recupera il valore della proprietà codSupportoId.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCodSupportoId() {
        return codSupportoId;
    }

    /**
     * Imposta il valore della proprietà codSupportoId.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCodSupportoId(String value) {
        this.codSupportoId = value;
    }

}
