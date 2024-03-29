package cnr.isti.sse.big.data.supporto;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;
import java.math.BigInteger;

@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
        "codice",
        "descrizione",
        "capoii",
        "capoiii",
        "iva",
        "isi",
        "isSPORT"
})
public class TabEvento {
    @XmlElement(name = "Codice", required = true)
    protected String codice;
    @XmlElement(name = "Descrizione", required = true)
    protected String descrizione;
    @XmlElement(name = "CAPOII")
    protected boolean capoii;
    @XmlElement(name = "CAPOIII")
    protected boolean capoiii;
    @XmlElement(name = "IVA", required = true)
    protected BigInteger iva;
    @XmlElement(name = "ISI", required = true)
    protected BigInteger isi;
    protected boolean isSPORT;

    /**
     * Recupera il valore della proprietÓ codice.
     *
     * @return
     *     possible object is
     *     {@link String }
     *
     */
    public String getCodice() {
        return codice;
    }

    /**
     * Imposta il valore della proprietÓ codice.
     *
     * @param value
     *     allowed object is
     *     {@link String }
     *
     */
    public void setCodice(String value) {
        this.codice = value;
    }

    /**
     * Recupera il valore della proprietÓ descrizione.
     *
     * @return
     *     possible object is
     *     {@link String }
     *
     */
    public String getDescrizione() {
        return descrizione;
    }

    /**
     * Imposta il valore della proprietÓ descrizione.
     *
     * @param value
     *     allowed object is
     *     {@link String }
     *
     */
    public void setDescrizione(String value) {
        this.descrizione = value;
    }

    /**
     * Recupera il valore della proprietÓ capoii.
     *
     */
    public boolean isCAPOII() {
        return capoii;
    }

    /**
     * Imposta il valore della proprietÓ capoii.
     *
     */
    public void setCAPOII(boolean value) {
        this.capoii = value;
    }

    /**
     * Recupera il valore della proprietÓ capoiii.
     *
     */
    public boolean isCAPOIII() {
        return capoiii;
    }

    /**
     * Imposta il valore della proprietÓ capoiii.
     *
     */
    public void setCAPOIII(boolean value) {
        this.capoiii = value;
    }

    /**
     * Recupera il valore della proprietÓ iva.
     *
     * @return
     *     possible object is
     *     {@link BigInteger }
     *
     */
    public BigInteger getIVA() {
        return iva;
    }

    /**
     * Imposta il valore della proprietÓ iva.
     *
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *
     */
    public void setIVA(BigInteger value) {
        this.iva = value;
    }

    /**
     * Recupera il valore della proprietÓ isi.
     *
     * @return
     *     possible object is
     *     {@link BigInteger }
     *
     */
    public BigInteger getISI() {
        return isi;
    }

    /**
     * Imposta il valore della proprietÓ isi.
     *
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *
     */
    public void setISI(BigInteger value) {
        this.isi = value;
    }

    /**
     * Recupera il valore della proprietÓ isSPORT.
     *
     */
    public boolean isIsSPORT() {
        return isSPORT;
    }

    /**
     * Imposta il valore della proprietÓ isSPORT.
     *
     */
    public void setIsSPORT(boolean value) {
        this.isSPORT = value;
    }

}

