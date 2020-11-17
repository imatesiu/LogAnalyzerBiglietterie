//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.2.8-b130911.1802 
// Vedere <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2020.11.17 alle 02:46:45 PM CET 
//


package cnr.isti.sse.big.data.riepilogogiornaliero;

import javax.xml.bind.JAXBElement;
import javax.xml.bind.annotation.XmlElementDecl;
import javax.xml.bind.annotation.XmlRegistry;
import javax.xml.namespace.QName;


/**
 * This object contains factory methods for each 
 * Java content interface and Java element interface 
 * generated in the cnr.isti.sse.big.data.riepilogogiornaliero package. 
 * <p>An ObjectFactory allows you to programatically 
 * construct new instances of the Java representation 
 * for XML content. The Java representation of XML 
 * content can consist of schema derived interfaces 
 * and classes representing the binding of schema 
 * type definitions, element declarations and model 
 * groups.  Factory methods for each of these are 
 * provided in this class.
 * 
 */
@XmlRegistry
public class ObjectFactory {

    private final static QName _ImportoPrestazione_QNAME = new QName("http://siae.it/gionaliero", "ImportoPrestazione");
    private final static QName _Data_QNAME = new QName("http://siae.it/gionaliero", "Data");
    private final static QName _CodiceOrdine_QNAME = new QName("http://siae.it/gionaliero", "CodiceOrdine");
    private final static QName _CodiceLocale_QNAME = new QName("http://siae.it/gionaliero", "CodiceLocale");
    private final static QName _QuantitaEventiAbilitati_QNAME = new QName("http://siae.it/gionaliero", "QuantitaEventiAbilitati");
    private final static QName _ImportoFigurativo_QNAME = new QName("http://siae.it/gionaliero", "ImportoFigurativo");
    private final static QName _Ora_QNAME = new QName("http://siae.it/gionaliero", "Ora");
    private final static QName _IVAFigurativa_QNAME = new QName("http://siae.it/gionaliero", "IVAFigurativa");
    private final static QName _IVAPrevendita_QNAME = new QName("http://siae.it/gionaliero", "IVAPrevendita");
    private final static QName _TipoTitolo_QNAME = new QName("http://siae.it/gionaliero", "TipoTitolo");
    private final static QName _Esecutore_QNAME = new QName("http://siae.it/gionaliero", "Esecutore");
    private final static QName _CodiceFiscale_QNAME = new QName("http://siae.it/gionaliero", "CodiceFiscale");
    private final static QName _SistemaEmissione_QNAME = new QName("http://siae.it/gionaliero", "SistemaEmissione");
    private final static QName _IncidenzaGenere_QNAME = new QName("http://siae.it/gionaliero", "IncidenzaGenere");
    private final static QName _Nazionalita_QNAME = new QName("http://siae.it/gionaliero", "Nazionalita");
    private final static QName _ProduttoreCinema_QNAME = new QName("http://siae.it/gionaliero", "ProduttoreCinema");
    private final static QName _Titolo_QNAME = new QName("http://siae.it/gionaliero", "Titolo");
    private final static QName _Capienza_QNAME = new QName("http://siae.it/gionaliero", "Capienza");
    private final static QName _IVACorrispettivo_QNAME = new QName("http://siae.it/gionaliero", "IVACorrispettivo");
    private final static QName _Incidenza_QNAME = new QName("http://siae.it/gionaliero", "Incidenza");
    private final static QName _Validita_QNAME = new QName("http://siae.it/gionaliero", "Validita");
    private final static QName _CorrispettivoLordo_QNAME = new QName("http://siae.it/gionaliero", "CorrispettivoLordo");
    private final static QName _CodiceAbbonamento_QNAME = new QName("http://siae.it/gionaliero", "CodiceAbbonamento");
    private final static QName _Prevendita_QNAME = new QName("http://siae.it/gionaliero", "Prevendita");
    private final static QName _Quantita_QNAME = new QName("http://siae.it/gionaliero", "Quantita");
    private final static QName _TipoGenere_QNAME = new QName("http://siae.it/gionaliero", "TipoGenere");
    private final static QName _Autore_QNAME = new QName("http://siae.it/gionaliero", "Autore");

    /**
     * Create a new ObjectFactory that can be used to create new instances of schema derived classes for package: cnr.isti.sse.big.data.riepilogogiornaliero
     * 
     */
    public ObjectFactory() {
    }

    /**
     * Create an instance of {@link Locale }
     * 
     */
    public Locale createLocale() {
        return new Locale();
    }

    /**
     * Create an instance of {@link Denominazione }
     * 
     */
    public Denominazione createDenominazione() {
        return new Denominazione();
    }

    /**
     * Create an instance of {@link TitoliAccessoIVAPreassolta }
     * 
     */
    public TitoliAccessoIVAPreassolta createTitoliAccessoIVAPreassolta() {
        return new TitoliAccessoIVAPreassolta();
    }

    /**
     * Create an instance of {@link MultiGenere }
     * 
     */
    public MultiGenere createMultiGenere() {
        return new MultiGenere();
    }

    /**
     * Create an instance of {@link TitoliOpere }
     * 
     */
    public TitoliOpere createTitoliOpere() {
        return new TitoliOpere();
    }

    /**
     * Create an instance of {@link AbbonamentiIVAPreassolta }
     * 
     */
    public AbbonamentiIVAPreassolta createAbbonamentiIVAPreassolta() {
        return new AbbonamentiIVAPreassolta();
    }

    /**
     * Create an instance of {@link Turno }
     * 
     */
    public Turno createTurno() {
        return new Turno();
    }

    /**
     * Create an instance of {@link Titolare }
     * 
     */
    public Titolare createTitolare() {
        return new Titolare();
    }

    /**
     * Create an instance of {@link AbbonamentiAnnullati }
     * 
     */
    public AbbonamentiAnnullati createAbbonamentiAnnullati() {
        return new AbbonamentiAnnullati();
    }

    /**
     * Create an instance of {@link BigliettiAbbonamento }
     * 
     */
    public BigliettiAbbonamento createBigliettiAbbonamento() {
        return new BigliettiAbbonamento();
    }

    /**
     * Create an instance of {@link TipoTassazione }
     * 
     */
    public TipoTassazione createTipoTassazione() {
        return new TipoTassazione();
    }

    /**
     * Create an instance of {@link TitoliAnnullati }
     * 
     */
    public TitoliAnnullati createTitoliAnnullati() {
        return new TitoliAnnullati();
    }

    /**
     * Create an instance of {@link Intrattenimento }
     * 
     */
    public Intrattenimento createIntrattenimento() {
        return new Intrattenimento();
    }

    /**
     * Create an instance of {@link Abbonamenti }
     * 
     */
    public Abbonamenti createAbbonamenti() {
        return new Abbonamenti();
    }

    /**
     * Create an instance of {@link AbbonamentiEmessi }
     * 
     */
    public AbbonamentiEmessi createAbbonamentiEmessi() {
        return new AbbonamentiEmessi();
    }

    /**
     * Create an instance of {@link AbbonamentiIVAPreassoltaAnnullati }
     * 
     */
    public AbbonamentiIVAPreassoltaAnnullati createAbbonamentiIVAPreassoltaAnnullati() {
        return new AbbonamentiIVAPreassoltaAnnullati();
    }

    /**
     * Create an instance of {@link BigliettiAbbonamentoAnnullati }
     * 
     */
    public BigliettiAbbonamentoAnnullati createBigliettiAbbonamentoAnnullati() {
        return new BigliettiAbbonamentoAnnullati();
    }

    /**
     * Create an instance of {@link Evento }
     * 
     */
    public Evento createEvento() {
        return new Evento();
    }

    /**
     * Create an instance of {@link OrdineDiPosto }
     * 
     */
    public OrdineDiPosto createOrdineDiPosto() {
        return new OrdineDiPosto();
    }

    /**
     * Create an instance of {@link TitoliAccesso }
     * 
     */
    public TitoliAccesso createTitoliAccesso() {
        return new TitoliAccesso();
    }

    /**
     * Create an instance of {@link TitoliIVAPreassoltaAnnullati }
     * 
     */
    public TitoliIVAPreassoltaAnnullati createTitoliIVAPreassoltaAnnullati() {
        return new TitoliIVAPreassoltaAnnullati();
    }

    /**
     * Create an instance of {@link RiepilogoGiornaliero }
     * 
     */
    public RiepilogoGiornaliero createRiepilogoGiornaliero() {
        return new RiepilogoGiornaliero();
    }

    /**
     * Create an instance of {@link Organizzatore }
     * 
     */
    public Organizzatore createOrganizzatore() {
        return new Organizzatore();
    }

    /**
     * Create an instance of {@link TipoOrganizzatore }
     * 
     */
    public TipoOrganizzatore createTipoOrganizzatore() {
        return new TipoOrganizzatore();
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "ImportoPrestazione")
    public JAXBElement<String> createImportoPrestazione(String value) {
        return new JAXBElement<String>(_ImportoPrestazione_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "Data")
    public JAXBElement<String> createData(String value) {
        return new JAXBElement<String>(_Data_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "CodiceOrdine")
    public JAXBElement<String> createCodiceOrdine(String value) {
        return new JAXBElement<String>(_CodiceOrdine_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "CodiceLocale")
    public JAXBElement<String> createCodiceLocale(String value) {
        return new JAXBElement<String>(_CodiceLocale_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "QuantitaEventiAbilitati")
    public JAXBElement<String> createQuantitaEventiAbilitati(String value) {
        return new JAXBElement<String>(_QuantitaEventiAbilitati_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "ImportoFigurativo")
    public JAXBElement<String> createImportoFigurativo(String value) {
        return new JAXBElement<String>(_ImportoFigurativo_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "Ora")
    public JAXBElement<String> createOra(String value) {
        return new JAXBElement<String>(_Ora_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "IVAFigurativa")
    public JAXBElement<String> createIVAFigurativa(String value) {
        return new JAXBElement<String>(_IVAFigurativa_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "IVAPrevendita")
    public JAXBElement<String> createIVAPrevendita(String value) {
        return new JAXBElement<String>(_IVAPrevendita_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "TipoTitolo")
    public JAXBElement<String> createTipoTitolo(String value) {
        return new JAXBElement<String>(_TipoTitolo_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "Esecutore")
    public JAXBElement<String> createEsecutore(String value) {
        return new JAXBElement<String>(_Esecutore_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "CodiceFiscale")
    public JAXBElement<String> createCodiceFiscale(String value) {
        return new JAXBElement<String>(_CodiceFiscale_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "SistemaEmissione")
    public JAXBElement<String> createSistemaEmissione(String value) {
        return new JAXBElement<String>(_SistemaEmissione_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "IncidenzaGenere")
    public JAXBElement<String> createIncidenzaGenere(String value) {
        return new JAXBElement<String>(_IncidenzaGenere_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "Nazionalita")
    public JAXBElement<String> createNazionalita(String value) {
        return new JAXBElement<String>(_Nazionalita_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "ProduttoreCinema")
    public JAXBElement<String> createProduttoreCinema(String value) {
        return new JAXBElement<String>(_ProduttoreCinema_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "Titolo")
    public JAXBElement<String> createTitolo(String value) {
        return new JAXBElement<String>(_Titolo_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "Capienza")
    public JAXBElement<String> createCapienza(String value) {
        return new JAXBElement<String>(_Capienza_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "IVACorrispettivo")
    public JAXBElement<String> createIVACorrispettivo(String value) {
        return new JAXBElement<String>(_IVACorrispettivo_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "Incidenza")
    public JAXBElement<String> createIncidenza(String value) {
        return new JAXBElement<String>(_Incidenza_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "Validita")
    public JAXBElement<String> createValidita(String value) {
        return new JAXBElement<String>(_Validita_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "CorrispettivoLordo")
    public JAXBElement<String> createCorrispettivoLordo(String value) {
        return new JAXBElement<String>(_CorrispettivoLordo_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "CodiceAbbonamento")
    public JAXBElement<String> createCodiceAbbonamento(String value) {
        return new JAXBElement<String>(_CodiceAbbonamento_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "Prevendita")
    public JAXBElement<String> createPrevendita(String value) {
        return new JAXBElement<String>(_Prevendita_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "Quantita")
    public JAXBElement<String> createQuantita(String value) {
        return new JAXBElement<String>(_Quantita_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "TipoGenere")
    public JAXBElement<String> createTipoGenere(String value) {
        return new JAXBElement<String>(_TipoGenere_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://siae.it/gionaliero", name = "Autore")
    public JAXBElement<String> createAutore(String value) {
        return new JAXBElement<String>(_Autore_QNAME, String.class, null, value);
    }

}
