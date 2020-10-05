//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.10.05 alle 12:50:22 PM CEST 
//


package cnr.isti.sse.big.data.transazioni;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.adapters.CollapsedStringAdapter;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;


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
 *         &lt;element ref="{}TitoloAccesso" minOccurs="0"/>
 *         &lt;element ref="{}Abbonamento" minOccurs="0"/>
 *         &lt;element ref="{}BigliettoAbbonamento" minOccurs="0"/>
 *         &lt;element ref="{}AcquirenteRegistrazione" minOccurs="0"/>
 *         &lt;element ref="{}AcquirenteTransazione" minOccurs="0"/>
 *         &lt;element ref="{}RiferimentoAnnullamento" minOccurs="0"/>
 *       &lt;/sequence>
 *       &lt;attribute name="CFOrganizzatore" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CFTitolare" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="IVAPreassolta" use="required">
 *         &lt;simpleType>
 *           &lt;restriction base="{http://www.w3.org/2001/XMLSchema}NMTOKEN">
 *             &lt;enumeration value="N"/>
 *             &lt;enumeration value="B"/>
 *             &lt;enumeration value="F"/>
 *           &lt;/restriction>
 *         &lt;/simpleType>
 *       &lt;/attribute>
 *       &lt;attribute name="TipoTassazione" use="required">
 *         &lt;simpleType>
 *           &lt;restriction base="{http://www.w3.org/2001/XMLSchema}NMTOKEN">
 *             &lt;enumeration value="S"/>
 *             &lt;enumeration value="I"/>
 *           &lt;/restriction>
 *         &lt;/simpleType>
 *       &lt;/attribute>
 *       &lt;attribute name="Valuta" default="E">
 *         &lt;simpleType>
 *           &lt;restriction base="{http://www.w3.org/2001/XMLSchema}NMTOKEN">
 *             &lt;enumeration value="E"/>
 *             &lt;enumeration value="L"/>
 *           &lt;/restriction>
 *         &lt;/simpleType>
 *       &lt;/attribute>
 *       &lt;attribute name="SistemaEmissione" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CartaAttivazione" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="SigilloFiscale" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="DataEmissione" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="OraEmissione" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="NumeroProgressivo" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="TipoTitolo" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CodiceOrdine" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="Causale" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="Posto" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CodiceRichiedenteEmissioneSigillo" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="Prestampa" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="ImponibileIntrattenimenti" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="OriginaleAnnullato" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CartaOriginaleAnnullato" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="CausaleAnnullamento" type="{http://www.w3.org/2001/XMLSchema}string" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "titoloAccesso",
    "abbonamento",
    "bigliettoAbbonamento",
    "acquirenteRegistrazione",
    "acquirenteTransazione",
    "riferimentoAnnullamento"
})
@XmlRootElement(name = "Transazione")
public class Transazione {

    @XmlElement(name = "TitoloAccesso")
    protected TitoloAccesso titoloAccesso;
    @XmlElement(name = "Abbonamento")
    protected Abbonamento abbonamento;
    @XmlElement(name = "BigliettoAbbonamento")
    protected BigliettoAbbonamento bigliettoAbbonamento;
    @XmlElement(name = "AcquirenteRegistrazione")
    protected AcquirenteRegistrazione acquirenteRegistrazione;
    @XmlElement(name = "AcquirenteTransazione")
    protected AcquirenteTransazione acquirenteTransazione;
    @XmlElement(name = "RiferimentoAnnullamento")
    protected RiferimentoAnnullamento riferimentoAnnullamento;
    @XmlAttribute(name = "CFOrganizzatore", required = true)
    protected String cfOrganizzatore;
    @XmlAttribute(name = "CFTitolare", required = true)
    protected String cfTitolare;
    @XmlAttribute(name = "IVAPreassolta", required = true)
    @XmlJavaTypeAdapter(CollapsedStringAdapter.class)
    protected String ivaPreassolta;
    @XmlAttribute(name = "TipoTassazione", required = true)
    @XmlJavaTypeAdapter(CollapsedStringAdapter.class)
    protected String tipoTassazione;
    @XmlAttribute(name = "Valuta")
    @XmlJavaTypeAdapter(CollapsedStringAdapter.class)
    protected String valuta;
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
    @XmlAttribute(name = "Causale")
    protected String causale;
    @XmlAttribute(name = "Posto")
    protected String posto;
    @XmlAttribute(name = "CodiceRichiedenteEmissioneSigillo", required = true)
    protected String codiceRichiedenteEmissioneSigillo;
    @XmlAttribute(name = "Prestampa")
    protected String prestampa;
    @XmlAttribute(name = "ImponibileIntrattenimenti")
    protected String imponibileIntrattenimenti;
    @XmlAttribute(name = "OriginaleAnnullato")
    protected String originaleAnnullato;
    @XmlAttribute(name = "CartaOriginaleAnnullato")
    protected String cartaOriginaleAnnullato;
    @XmlAttribute(name = "CausaleAnnullamento")
    protected String causaleAnnullamento;

    /**
     * Recupera il valore della proprietà titoloAccesso.
     * 
     * @return
     *     possible object is
     *     {@link TitoloAccesso }
     *     
     */
    public TitoloAccesso getTitoloAccesso() {
        return titoloAccesso;
    }

    /**
     * Imposta il valore della proprietà titoloAccesso.
     * 
     * @param value
     *     allowed object is
     *     {@link TitoloAccesso }
     *     
     */
    public void setTitoloAccesso(TitoloAccesso value) {
        this.titoloAccesso = value;
    }

    /**
     * Recupera il valore della proprietà abbonamento.
     * 
     * @return
     *     possible object is
     *     {@link Abbonamento }
     *     
     */
    public Abbonamento getAbbonamento() {
        return abbonamento;
    }

    /**
     * Imposta il valore della proprietà abbonamento.
     * 
     * @param value
     *     allowed object is
     *     {@link Abbonamento }
     *     
     */
    public void setAbbonamento(Abbonamento value) {
        this.abbonamento = value;
    }

    /**
     * Recupera il valore della proprietà bigliettoAbbonamento.
     * 
     * @return
     *     possible object is
     *     {@link BigliettoAbbonamento }
     *     
     */
    public BigliettoAbbonamento getBigliettoAbbonamento() {
        return bigliettoAbbonamento;
    }

    /**
     * Imposta il valore della proprietà bigliettoAbbonamento.
     * 
     * @param value
     *     allowed object is
     *     {@link BigliettoAbbonamento }
     *     
     */
    public void setBigliettoAbbonamento(BigliettoAbbonamento value) {
        this.bigliettoAbbonamento = value;
    }

    /**
     * Recupera il valore della proprietà acquirenteRegistrazione.
     * 
     * @return
     *     possible object is
     *     {@link AcquirenteRegistrazione }
     *     
     */
    public AcquirenteRegistrazione getAcquirenteRegistrazione() {
        return acquirenteRegistrazione;
    }

    /**
     * Imposta il valore della proprietà acquirenteRegistrazione.
     * 
     * @param value
     *     allowed object is
     *     {@link AcquirenteRegistrazione }
     *     
     */
    public void setAcquirenteRegistrazione(AcquirenteRegistrazione value) {
        this.acquirenteRegistrazione = value;
    }

    /**
     * Recupera il valore della proprietà acquirenteTransazione.
     * 
     * @return
     *     possible object is
     *     {@link AcquirenteTransazione }
     *     
     */
    public AcquirenteTransazione getAcquirenteTransazione() {
        return acquirenteTransazione;
    }

    /**
     * Imposta il valore della proprietà acquirenteTransazione.
     * 
     * @param value
     *     allowed object is
     *     {@link AcquirenteTransazione }
     *     
     */
    public void setAcquirenteTransazione(AcquirenteTransazione value) {
        this.acquirenteTransazione = value;
    }

    /**
     * Recupera il valore della proprietà riferimentoAnnullamento.
     * 
     * @return
     *     possible object is
     *     {@link RiferimentoAnnullamento }
     *     
     */
    public RiferimentoAnnullamento getRiferimentoAnnullamento() {
        return riferimentoAnnullamento;
    }

    /**
     * Imposta il valore della proprietà riferimentoAnnullamento.
     * 
     * @param value
     *     allowed object is
     *     {@link RiferimentoAnnullamento }
     *     
     */
    public void setRiferimentoAnnullamento(RiferimentoAnnullamento value) {
        this.riferimentoAnnullamento = value;
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
     * Recupera il valore della proprietà ivaPreassolta.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIVAPreassolta() {
        return ivaPreassolta;
    }

    /**
     * Imposta il valore della proprietà ivaPreassolta.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIVAPreassolta(String value) {
        this.ivaPreassolta = value;
    }

    /**
     * Recupera il valore della proprietà tipoTassazione.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTipoTassazione() {
        return tipoTassazione;
    }

    /**
     * Imposta il valore della proprietà tipoTassazione.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTipoTassazione(String value) {
        this.tipoTassazione = value;
    }

    /**
     * Recupera il valore della proprietà valuta.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getValuta() {
        if (valuta == null) {
            return "E";
        } else {
            return valuta;
        }
    }

    /**
     * Imposta il valore della proprietà valuta.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setValuta(String value) {
        this.valuta = value;
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
     * Recupera il valore della proprietà causale.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCausale() {
        return causale;
    }

    /**
     * Imposta il valore della proprietà causale.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCausale(String value) {
        this.causale = value;
    }

    /**
     * Recupera il valore della proprietà posto.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getPosto() {
        return posto;
    }

    /**
     * Imposta il valore della proprietà posto.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setPosto(String value) {
        this.posto = value;
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
     * Recupera il valore della proprietà prestampa.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getPrestampa() {
        return prestampa;
    }

    /**
     * Imposta il valore della proprietà prestampa.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setPrestampa(String value) {
        this.prestampa = value;
    }

    /**
     * Recupera il valore della proprietà imponibileIntrattenimenti.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getImponibileIntrattenimenti() {
        return imponibileIntrattenimenti;
    }

    /**
     * Imposta il valore della proprietà imponibileIntrattenimenti.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setImponibileIntrattenimenti(String value) {
        this.imponibileIntrattenimenti = value;
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
