package cnr.isti.sse.big.rest.impl;
import java.io.InputStream;
import java.io.StringReader;
import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.ws.rs.Consumes;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Unmarshaller;

import org.apache.commons.io.IOUtils;
import org.glassfish.jersey.media.multipart.FormDataBodyPart;
import org.glassfish.jersey.media.multipart.FormDataContentDisposition;
import org.glassfish.jersey.media.multipart.FormDataParam;

import cnr.isti.sse.big.data.reply.accessi.lta.LTAGiornaliera;
import cnr.isti.sse.big.data.transazioni.LogTransazione;
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
public class ApiRestLTA {

	private static  org.apache.logging.log4j.Logger log = org.apache.logging.log4j.LogManager.getLogger(ApiRestLTA.class);

	

	@Path("/ListLTA")
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
			mediaType = MediaType.MULTIPART_FORM_DATA//,
			//	schema = @Schema(implementation = List<byte[]>.class)
			),
	description = "." )
	@Consumes(MediaType.MULTIPART_FORM_DATA)
	//@Produces(MediaType.APPLICATION_JSON)
	public String putLogTransazioneFiles( @FormDataParam("files") List<FormDataBodyPart> uploadedInputStream,
			@FormDataParam("files") List<FormDataContentDisposition> fileDetail, @Context HttpServletRequest request, @Context HttpServletResponse response)
					throws JAXBException {// DatiCorrispettiviType Corrispettivi,
		// @Context HttpServletRequest request){
		response.setHeader("Connection", "Close");
		log.info("****************List***LTA********************");
		try{

			log.info("Message from: "+request.getRemoteAddr());




			for(FormDataBodyPart filePart: uploadedInputStream) {
				byte[] your_primitive_bytes = IOUtils.toByteArray(filePart.getEntityAs(InputStream.class));




				boolean	resul = Utility.verifyPKCS7(your_primitive_bytes);
				log.info(resul);

				byte[] t = 	Utility.getData(your_primitive_bytes);
				String LogTransazione = new String(t);
				String LT = LogTransazione.replaceAll("<!DOCTYPE LTA_Giornaliera SYSTEM.*", "").replaceAll("[^\\x20-\\x7e]", "");
				JAXBContext jaxbContext = JAXBContext.newInstance(LTAGiornaliera.class);
				Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
				Utility.validateXmlLogTransazione(unmarshaller);	

				StringReader reader = new StringReader(LT);
				LTAGiornaliera LogT = (LTAGiornaliera) unmarshaller.unmarshal(reader);

				
			}
			//log.info("Logs: [NProgressivi, Corrispettivo Lordo, Prevendita Lordo] "+sum);
			String text = "KO";
			return text;//new Log(sum);
			//throw new WebApplicationException(Response.status(406).entity(text).build());



		} catch (Exception e) {
			e.printStackTrace();
			log.error(e);
		}
		return null;
		//return "";

	}

	/*@Path("/SingleFileLTA")
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
			mediaType = MediaType.MULTIPART_FORM_DATA//,
			//	schema = @Schema(implementation = List<byte[]>.class)
			),
	description = "." )
	@Consumes(MediaType.MULTIPART_FORM_DATA)
	public String putLogTransazionel( @FormDataParam("file") InputStream uploadedInputStream,
			@FormDataParam("file") FormDataContentDisposition fileDetail, @Context HttpServletRequest request, @Context HttpServletResponse response)
					throws JAXBException {// DatiCorrispettiviType Corrispettivi,
		// @Context HttpServletRequest request){
		response.setHeader("Connection", "Close");
		log.info("****************FileRiepilogoControlloAccessi********************");
		try{

			log.info("Message from: "+request.getRemoteAddr());


			String text = "KO";
			return text;
			//throw new WebApplicationException(Response.status(406).entity(text).build());



		} catch (Exception e) {
			e.printStackTrace();
			log.error(e);
		}
		return "";

	}*/



	

}
