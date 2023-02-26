package cnr.isti.sse.big.data.supporto;

import cnr.isti.sse.big.rest.impl.ApiRestRPGBig;

import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Unmarshaller;
import java.io.InputStream;

import static org.junit.Assert.assertNotNull;

public class ReadTabEventiIntegrata {

    private static  org.apache.logging.log4j.Logger log = org.apache.logging.log4j.LogManager.getLogger(ReadTabEventiIntegrata.class);


    public static TabEventiIntegrata readTabEventi(){
        InputStream is = ReadTabEventiIntegrata.class.getClassLoader().getResourceAsStream("TabEventi.xml");
        assertNotNull(is);

        JAXBContext jaxbContext;
        try {
            jaxbContext = JAXBContext.newInstance(TabEventiIntegrata.class);

            Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
            //StringReader reader = new StringReader(EsitoOperazione);

            TabEventiIntegrata TEsitoOperazione = (TabEventiIntegrata) unmarshaller.unmarshal(is);

            return TEsitoOperazione;
        } catch (JAXBException e) {
            log.error(e.getLocalizedMessage());
        }
        return null;
    }

}
