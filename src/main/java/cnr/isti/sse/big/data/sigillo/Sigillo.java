//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.10.05 alle 12:49:52 PM CEST 
//


package cnr.isti.sse.big.data.sigillo;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.XmlValue;


/**
 * <p>Classe Java per anonymous complex type.
 * 
 * <p>Il seguente frammento di schema specifica il contenuto previsto contenuto in questa classe.
 * 
 * <pre>
 * &lt;complexType>
 *   &lt;simpleContent>
 *     &lt;extension base="&lt;http://www.w3.org/2001/XMLSchema>string">
 *       &lt;attribute name="CFOrganizzatore" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CFTitolare" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="SistemaEmissione" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CartaAttivazione" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="SigilloFiscale" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="DataEmissione" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="OraEmissione" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="NumeroProgressivo" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="TipoTitolo" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CodiceOrdine" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CorrispettivoLordo" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CodiceRichiedenteEmissioneSigillo" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="OriginaleAnnullato" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CartaOriginaleAnnullato" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CausaleAnnullamento" type="{http://www.w3.org/2001/XMLSchema}string" />
 *     &lt;/extension>
 *   &lt;/simpleContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "value"
})
@XmlRootElement(name = "Sigillo")
public class Sigillo {

    @XmlValue
    protected String value;
    @XmlAttribute(name = "CFOrganizzatore", required = true)
    protected String cfOrganizzatore;
    @XmlAttribute(name = "CFTitolare", required = true)
    protected String cfTitolare;
    @XmlAttribute(name = "SistemaEmissione", required = true)
    protected String sistemaEmissione;
    @XmlAttribute(name = "CartaAttivazione", required = true)
    protected String cartaAttivazione;
    @XmlAttribute(name = "SigilloFiscale", required = true)
    protected String sigilloFiscale;
    @XmlAttribute(name = "DataEmissione", required = true)
    protected String dataEmissione;
    @XmlAttribute(name = "OraEmissione", required = true)
    protected String oraEmissione;
    @XmlAttribute(name = "NumeroProgressivo", required = true)
    protected String numeroProgressivo;
    @XmlAttribute(name = "TipoTitolo", required = true)
    protected String tipoTitolo;
    @XmlAttribute(name = "CodiceOrdine", required = true)
    protected String codiceOrdine;
    @XmlAttribute(name = "CorrispettivoLordo", required = true)
    protected String corrispettivoLordo;
    @XmlAttribute(name = "CodiceRichiedenteEmissioneSigillo", required = true)
    protected String codiceRichiedenteEmissioneSigillo;
    @XmlAttribute(name = "OriginaleAnnullato")
    protected String originaleAnnullato;
    @XmlAttribute(name = "CartaOriginaleAnnullato")
    protected String cartaOriginaleAnnullato;
    @XmlAttribute(name = "CausaleAnnullamento")
    protected String causaleAnnullamento;

    /**
     * Recupera il valore della proprietà value.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getValue() {
        return value;
    }

    /**
     * Imposta il valore della proprietà value.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setValue(String value) {
        this.value = value;
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
     * Recupera il valore della proprietà cfTitolare.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCFTitolare() {
        return cfTitolare;
    }

    /**
     * Imposta il valore della proprietà cfTitolare.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCFTitolare(String value) {
        this.cfTitolare = value;
    }

    /**
     * Recupera il valore della proprietà sistemaEmissione.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getSistemaEmissione() {
        return sistemaEmissione;
    }

    /**
     * Imposta il valore della proprietà sistemaEmissione.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSistemaEmissione(String value) {
        this.sistemaEmissione = value;
    }

    /**
     * Recupera il valore della proprietà cartaAttivazione.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCartaAttivazione() {
        return cartaAttivazione;
    }

    /**
     * Imposta il valore della proprietà cartaAttivazione.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCartaAttivazione(String value) {
        this.cartaAttivazione = value;
    }

    /**
     * Recupera il valore della proprietà sigilloFiscale.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getSigilloFiscale() {
        return sigilloFiscale;
    }

    /**
     * Imposta il valore della proprietà sigilloFiscale.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSigilloFiscale(String value) {
        this.sigilloFiscale = value;
    }

    /**
     * Recupera il valore della proprietà dataEmissione.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDataEmissione() {
        return dataEmissione;
    }

    /**
     * Imposta il valore della proprietà dataEmissione.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDataEmissione(String value) {
        this.dataEmissione = value;
    }

    /**
     * Recupera il valore della proprietà oraEmissione.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getOraEmissione() {
        return oraEmissione;
    }

    /**
     * Imposta il valore della proprietà oraEmissione.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setOraEmissione(String value) {
        this.oraEmissione = value;
    }

    /**
     * Recupera il valore della proprietà numeroProgressivo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getNumeroProgressivo() {
        return numeroProgressivo;
    }

    /**
     * Imposta il valore della proprietà numeroProgressivo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setNumeroProgressivo(String value) {
        this.numeroProgressivo = value;
    }

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
     * Recupera il valore della proprietà corrispettivoLordo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCorrispettivoLordo() {
        return corrispettivoLordo;
    }

    /**
     * Imposta il valore della proprietà corrispettivoLordo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCorrispettivoLordo(String value) {
        this.corrispettivoLordo = value;
    }

    /**
     * Recupera il valore della proprietà codiceRichiedenteEmissioneSigillo.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCodiceRichiedenteEmissioneSigillo() {
        return codiceRichiedenteEmissioneSigillo;
    }

    /**
     * Imposta il valore della proprietà codiceRichiedenteEmissioneSigillo.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCodiceRichiedenteEmissioneSigillo(String value) {
        this.codiceRichiedenteEmissioneSigillo = value;
    }

    /**
     * Recupera il valore della proprietà originaleAnnullato.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getOriginaleAnnullato() {
        return originaleAnnullato;
    }

    /**
     * Imposta il valore della proprietà originaleAnnullato.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setOriginaleAnnullato(String value) {
        this.originaleAnnullato = value;
    }

    /**
     * Recupera il valore della proprietà cartaOriginaleAnnullato.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCartaOriginaleAnnullato() {
        return cartaOriginaleAnnullato;
    }

    /**
     * Imposta il valore della proprietà cartaOriginaleAnnullato.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCartaOriginaleAnnullato(String value) {
        this.cartaOriginaleAnnullato = value;
    }

    /**
     * Recupera il valore della proprietà causaleAnnullamento.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCausaleAnnullamento() {
        return causaleAnnullamento;
    }

    /**
     * Imposta il valore della proprietà causaleAnnullamento.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCausaleAnnullamento(String value) {
        this.causaleAnnullamento = value;
    }

}
