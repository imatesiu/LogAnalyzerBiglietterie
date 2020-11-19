package cnr.isti.sse.big.rest.impl;
import java.io.InputStream;
import java.io.StringReader;
import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.ws.rs.Consumes;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Unmarshaller;

import org.apache.commons.io.IOUtils;
import org.glassfish.jersey.media.multipart.FormDataBodyPart;
import org.glassfish.jersey.media.multipart.FormDataContentDisposition;
import org.glassfish.jersey.media.multipart.FormDataParam;

import cnr.isti.sse.big.data.reply.rp.LogRP;
import cnr.isti.sse.big.data.riepilogogiornaliero.RiepilogoGiornaliero;
import cnr.isti.sse.big.data.riepilogomensile.Organizzatore;
import cnr.isti.sse.big.util.Utility;
import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.parameters.RequestBody;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.servers.Server;



@OpenAPIDefinition(info = @Info(title = "APID Service", version = "0.1"), servers = {@Server(url="/v1/dispositivi")
})
//@Consumes(MediaType.MULTIPART_FORM_DATA)
// @Produces(MediaType.APPLICATION_XML)
@Path("/biglietterie")
public class ApiRestRPGBig {

	private static  org.apache.logging.log4j.Logger log = org.apache.logging.log4j.LogManager.getLogger(ApiRestRPGBig.class);

	/*@Path("/RPG")
	@POST
	@ApiResponse(
			responseCode = "200",
			content = @Content(
					mediaType = MediaType.APPLICATION_XML,
					schema = @Schema(implementation = String.class)
					),
			description = "."
			)
	@RequestBody(content = @Content(
			mediaType = MediaType.MULTIPART_FORM_DATA,
			schema = @Schema(implementation = RiepilogoGiornaliero.class)
			),
	description = "." )
	public String putRPG(byte[] rpg, @Context HttpServletRequest request, @Context HttpServletResponse response)
			throws JAXBException {// DatiCorrispettiviType Corrispettivi,
		// @Context HttpServletRequest request){
		response.setHeader("Connection", "Close");
		log.info("****************RPG********************");
		try{

			log.info("Message from: "+request.getRemoteAddr());

			boolean	result = Utility.verifyPKCS7(rpg);
			log.info(result);

			byte[] t = 	Utility.getData(rpg);
			String rgiorna = new String(t);
			String giorna = rgiorna.replaceAll("<!DOCTYPE RiepilogoGiornaliero SYSTEM.*", "");


			JAXBContext jaxbContext = JAXBContext.newInstance(RiepilogoGiornaliero.class);
			Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
			Utility.validateXmlLogTransazione(unmarshaller);	

			StringReader reader = new StringReader(giorna);
			RiepilogoGiornaliero RPG = (RiepilogoGiornaliero) unmarshaller.unmarshal(reader);

			List<Organizzatore> organizzatori = RPG.getOrganizzatore();


			Utility.check(organizzatori);

			//Utility.check(LogT);

			String text = "KO";
			return text;
			//throw new WebApplicationException(Response.status(406).entity(text).build());



		} catch (Exception e) {
			e.printStackTrace();
			log.error(e);
		}
		return "";

	}*/


	@Path("/ListRiepilogoGiornaliero")
	@POST
	@ApiResponse(
			responseCode = "200",
			content = @Content(
					mediaType = MediaType.APPLICATION_XML,
					schema = @Schema(implementation = String.class)
					),
			description = "."
			)
	@RequestBody(content = @Content(
			mediaType = MediaType.MULTIPART_FORM_DATA,
			schema = @Schema(implementation = RiepilogoGiornaliero.class)
			),
	description = "." )
	@Consumes(MediaType.MULTIPART_FORM_DATA)
	@Produces(MediaType.APPLICATION_JSON)
	public LogRP putListRPG(@FormDataParam("files") List<FormDataBodyPart> uploadedInputStream,
			@FormDataParam("files") List<FormDataContentDisposition> fileDetail, @Context HttpServletRequest request, @Context HttpServletResponse response)
					throws JAXBException {// DatiCorrispettiviType Corrispettivi,
		// @Context HttpServletRequest request){
		response.setHeader("Connection", "Close");
		log.info("****************List***RPG********************");
		try{

			log.info("Message from: "+request.getRemoteAddr());
			LogRP f = new LogRP();
			for(FormDataBodyPart filePart: uploadedInputStream) {
				byte[] your_primitive_bytes = IOUtils.toByteArray(filePart.getEntityAs(InputStream.class));
				boolean	result = Utility.verifyPKCS7(your_primitive_bytes);
				log.info(result);

				byte[] t = 	Utility.getData(your_primitive_bytes);
				String rgiorna = new String(t);
				String giorna = rgiorna.replaceAll("<!DOCTYPE RiepilogoGiornaliero SYSTEM.*", "");


				JAXBContext jaxbContext = JAXBContext.newInstance(RiepilogoGiornaliero.class);
				Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
				Utility.validateXmlLogTransazione(unmarshaller);	

				StringReader reader = new StringReader(giorna);
				RiepilogoGiornaliero RPG = (RiepilogoGiornaliero) unmarshaller.unmarshal(reader);

				List<Organizzatore> organizzatori = RPG.getOrganizzatore();


				LogRP  l  =  Utility.check(organizzatori);
				f.update(l);
				//Utility.check(LogT);
			}
			
			String text = "KO";
			return f;//text;
			//throw new WebApplicationException(Response.status(406).entity(text).build());



		} catch (Exception e) {
			e.printStackTrace();
			log.error(e);
		}
		return null;

	}



}
